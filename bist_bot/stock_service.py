from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import math
import unicodedata
import warnings
from zoneinfo import ZoneInfo

import borsapy as bp
import pandas as pd

from bist_bot.company_context import get_company_context
from bist_bot.i18n import t


warnings.filterwarnings(
    "ignore",
    message="Workbook contains no default style, apply openpyxl's default",
)


TURKISH_TEXT_FIXES = str.maketrans(
    {
        "Ý": "İ",
        "ý": "ı",
        "Ð": "Ğ",
        "ð": "ğ",
        "Þ": "Ş",
        "þ": "ş",
        "Ţ": "Ş",
        "ţ": "ş",
        "Đ": "Ğ",
        "đ": "ğ",
    }
)

TURKISH_ASCII = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


@dataclass(frozen=True)
class CompanyCandidate:
    ticker: str
    name: str
    city: str | None


@dataclass(frozen=True)
class StockSnapshot:
    symbol: str
    company_name: str
    city: str | None
    sector: str | None
    industry: str | None
    website: str | None
    business_summary: str | None
    context_notes: list[str]
    last_price: float | None
    change_percent: float | None
    change_amount: float | None
    open_price: float | None
    day_high: float | None
    day_low: float | None
    volume: float | None
    market_cap: float | None
    pe_ratio: float | None
    pb_ratio: float | None
    year_high: float | None
    year_low: float | None
    fifty_day_average: float | None
    two_hundred_day_average: float | None
    foreign_ratio: float | None
    free_float: float | None
    net_debt: float | None
    last_update: datetime | None
    month_change_percent: float | None
    month_high: float | None
    month_low: float | None
    month_average_volume: float | None
    revenue_latest: float | None
    revenue_previous: float | None
    revenue_growth_percent: float | None
    gross_profit_latest: float | None
    net_income_latest: float | None
    operating_cashflow_latest: float | None
    analyst_targets: dict[str, float | int | None]
    recent_kap: list[str]
    upcoming_calendar: list[str]
    realtime_enabled: bool
    financial_year: str


class CompanyLookupError(RuntimeError):
    """Raised when a company cannot be resolved uniquely."""

    def __init__(
        self,
        code: str,
        message: str,
        candidates: list[CompanyCandidate] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.candidates = candidates or []


def configure_tradingview_auth(
    username: str | None,
    password: str | None,
    session: str | None,
    session_sign: str | None,
) -> bool:
    if username and password:
        bp.set_tradingview_auth(username=username, password=password)
        return True

    if session:
        bp.set_tradingview_auth(session=session, session_sign=session_sign)
        return True

    return False


def find_company_candidates(query: str, limit: int = 5) -> list[CompanyCandidate]:
    df = bp.search_companies(query.strip())
    if df is None or df.empty:
        return []

    deduped = df.drop_duplicates(subset=["ticker"]).head(limit)
    return [
        CompanyCandidate(
            ticker=clean_text(row.get("ticker")) or "",
            name=clean_text(row.get("name")) or "",
            city=clean_text(row.get("city")),
        )
        for _, row in deduped.iterrows()
    ]


def resolve_symbol(query: str) -> CompanyCandidate:
    cleaned_query = clean_text(query or "")
    if not cleaned_query:
        raise CompanyLookupError("empty_query", "Bos sorgu gonderildi.")

    candidates = find_company_candidates(cleaned_query, limit=8)
    normalized_query = normalize_symbol(cleaned_query)

    exact_ticker = [item for item in candidates if normalize_symbol(item.ticker) == normalized_query]
    if exact_ticker:
        return exact_ticker[0]

    exact_name = [item for item in candidates if normalize_key(item.name) == normalize_key(cleaned_query)]
    if exact_name:
        return exact_name[0]

    if len(candidates) == 1:
        return candidates[0]

    if len(candidates) > 1:
        raise CompanyLookupError("ambiguous", "Birden fazla eslesme bulundu.", candidates=candidates[:5])

    if looks_like_ticker(cleaned_query):
        ticker = normalize_symbol(cleaned_query)
        return CompanyCandidate(ticker=ticker, name=ticker, city=None)

    raise CompanyLookupError("not_found", "Sirket bulunamadi.")


def build_snapshot(query: str, realtime_enabled: bool) -> StockSnapshot:
    candidate = resolve_symbol(query)
    stock = bp.Ticker(candidate.ticker)

    info = stock.info.todict()
    history = safe_load(lambda: stock.history(period="1mo"), pd.DataFrame())
    income_stmt = safe_load(lambda: stock.income_stmt, pd.DataFrame())
    cashflow = safe_load(lambda: stock.cashflow, pd.DataFrame())
    news = safe_load(lambda: stock.news, pd.DataFrame())
    calendar = safe_load(lambda: stock.calendar, pd.DataFrame())
    analyst_targets = safe_load(lambda: stock.analyst_price_targets, {}) or {}

    company_name = clean_text(info.get("description")) or candidate.name or candidate.ticker
    month_change_percent = None
    month_high = None
    month_low = None
    month_average_volume = None

    if history is not None and not history.empty:
        close_start = to_float(history["Close"].iloc[0])
        close_end = to_float(history["Close"].iloc[-1])
        if close_start not in (None, 0) and close_end is not None:
            month_change_percent = ((close_end - close_start) / close_start) * 100

        month_high = to_float(history["High"].max())
        month_low = to_float(history["Low"].min())
        month_average_volume = to_float(history["Volume"].mean())

    current_year, previous_year = latest_two_columns(income_stmt)
    financial_year = str(current_year) if current_year is not None else "Latest"

    revenue_latest = pick_statement_value(income_stmt, current_year, ["Satış Gelirleri"])
    revenue_previous = pick_statement_value(income_stmt, previous_year, ["Satış Gelirleri"])
    revenue_growth_percent = growth_percent(revenue_latest, revenue_previous)
    gross_profit_latest = pick_statement_value(
        income_stmt,
        current_year,
        ["BRÜT KAR (ZARAR)", "Ticari Faaliyetlerden Brüt Kar (Zarar)"],
    )
    net_income_latest = pick_statement_value(
        income_stmt,
        current_year,
        ["DÖNEM KARI (ZARARI)", "SÜRDÜRÜLEN FAALİYETLER DÖNEM KARI/ZARARI"],
    )
    operating_cashflow_latest = pick_statement_value(
        cashflow,
        current_year,
        ["İşletme Faaliyetlerinden Kaynaklanan Net Nakit"],
    )

    return StockSnapshot(
        symbol=candidate.ticker,
        company_name=company_name,
        city=candidate.city,
        sector=clean_text(info.get("sector")),
        industry=clean_text(info.get("industry")),
        website=clean_text(info.get("website")),
        business_summary=compact_summary(clean_text(info.get("longBusinessSummary"))),
        context_notes=get_company_context(candidate.ticker, "tr"),
        last_price=to_float(info.get("last")),
        change_percent=to_float(info.get("change_percent")),
        change_amount=to_float(info.get("change")),
        open_price=to_float(info.get("open")),
        day_high=to_float(info.get("high")),
        day_low=to_float(info.get("low")),
        volume=to_float(info.get("volume")),
        market_cap=to_float(info.get("marketCap")),
        pe_ratio=to_float(info.get("trailingPE")),
        pb_ratio=to_float(info.get("priceToBook")),
        year_high=to_float(info.get("fiftyTwoWeekHigh")),
        year_low=to_float(info.get("fiftyTwoWeekLow")),
        fifty_day_average=to_float(info.get("fiftyDayAverage")),
        two_hundred_day_average=to_float(info.get("twoHundredDayAverage")),
        foreign_ratio=to_float(info.get("foreignRatio")),
        free_float=to_float(info.get("floatShares")),
        net_debt=to_float(info.get("netDebt")),
        last_update=parse_timestamp(info.get("timestamp")),
        month_change_percent=month_change_percent,
        month_high=month_high,
        month_low=month_low,
        month_average_volume=month_average_volume,
        revenue_latest=revenue_latest,
        revenue_previous=revenue_previous,
        revenue_growth_percent=revenue_growth_percent,
        gross_profit_latest=gross_profit_latest,
        net_income_latest=net_income_latest,
        operating_cashflow_latest=operating_cashflow_latest,
        analyst_targets=dict(analyst_targets),
        recent_kap=build_recent_kap(news),
        upcoming_calendar=build_upcoming_calendar(calendar),
        realtime_enabled=realtime_enabled,
        financial_year=financial_year,
    )


def build_recent_kap(news: pd.DataFrame | None, limit: int = 3) -> list[str]:
    if news is None or news.empty:
        return []

    items: list[str] = []
    for _, row in news.head(limit).iterrows():
        date_text = clean_text(row.get("Date")) or "-"
        title = clean_text(row.get("Title")) or "-"
        items.append(f"{date_text}: {title}")
    return items


def build_upcoming_calendar(calendar: pd.DataFrame | None, limit: int = 3) -> list[str]:
    if calendar is None or calendar.empty:
        return []

    items: list[str] = []
    for _, row in calendar.head(limit).iterrows():
        start = clean_text(row.get("StartDate")) or "-"
        end = clean_text(row.get("EndDate")) or "-"
        subject = clean_text(row.get("Subject")) or "-"
        period = clean_text(row.get("Period")) or ""
        suffix = f" ({period})" if period else ""
        items.append(f"{start} - {end}: {subject}{suffix}")
    return items


def latest_two_columns(df: pd.DataFrame | None) -> tuple[str | int | None, str | int | None]:
    if df is None or df.empty:
        return None, None
    columns = list(df.columns)
    return columns[0], columns[1] if len(columns) > 1 else None


def pick_statement_value(
    df: pd.DataFrame | None,
    column: str | int | None,
    row_candidates: list[str],
) -> float | None:
    if df is None or df.empty or column is None:
        return None

    normalized_rows = {normalize_key(index): index for index in df.index}
    for candidate in row_candidates:
        matched_row = normalized_rows.get(normalize_key(candidate))
        if matched_row is not None:
            return to_float(df.loc[matched_row, column])
    return None


def clean_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).translate(TURKISH_TEXT_FIXES).strip()
    return " ".join(text.split()) if text else None


def compact_summary(value: str | None, max_length: int = 320) -> str | None:
    if not value:
        return None
    cleaned = value.replace("u0026nbsp;", " ").strip()
    if len(cleaned) <= max_length:
        return cleaned
    return cleaned[: max_length - 3].rstrip() + "..."


def safe_load(loader, default):
    try:
        return loader()
    except Exception:
        return default


def normalize_symbol(value: str) -> str:
    return clean_text(value).upper().replace(".IS", "").replace(".E", "")  # type: ignore[union-attr]


def looks_like_ticker(value: str) -> bool:
    normalized = normalize_symbol(value)
    return normalized.isalnum() and 2 <= len(normalized) <= 6


def normalize_key(value: object) -> str:
    text = clean_text(value) or ""
    text = text.translate(TURKISH_ASCII)
    text = unicodedata.normalize("NFKD", text)
    return "".join(char.lower() for char in text if char.isalnum())


def to_float(value: object) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number):
        return None
    return number


def parse_timestamp(value: object) -> datetime | None:
    if value is None:
        return None
    try:
        timestamp = int(value)
    except (TypeError, ValueError):
        return None
    return datetime.fromtimestamp(timestamp, tz=ZoneInfo("Europe/Istanbul"))


def growth_percent(current: float | None, previous: float | None) -> float | None:
    if current is None or previous in (None, 0):
        return None
    return ((current - previous) / previous) * 100


def format_price(value: float | None, language: str = "tr") -> str:
    if value is None:
        return "-"
    if language == "tr":
        return f"{value:,.2f} TL".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{value:,.2f} TRY"


def format_percent(value: float | None, language: str = "tr") -> str:
    if value is None:
        return "-"
    if language == "tr":
        return f"%{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{value:,.2f}%"


def format_number(value: float | None, language: str = "tr") -> str:
    if value is None:
        return "-"
    if language == "tr":
        return f"{value:,.0f}".replace(",", ".")
    return f"{value:,.0f}"


def format_compact_currency(value: float | None, language: str = "tr") -> str:
    if value is None:
        return "-"

    abs_value = abs(value)
    if abs_value >= 1_000_000_000:
        divisor = 1_000_000_000
        suffix = " mlr TL" if language == "tr" else " bn TRY"
    elif abs_value >= 1_000_000:
        divisor = 1_000_000
        suffix = " mn TL" if language == "tr" else " mn TRY"
    else:
        divisor = 1
        suffix = " TL" if language == "tr" else " TRY"

    compact = value / divisor
    if language == "tr":
        return f"{compact:,.2f}{suffix}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{compact:,.2f}{suffix}"


def format_numeric_ratio(value: float | None, language: str = "tr") -> str:
    if value is None:
        return "-"
    if language == "tr":
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{value:,.2f}"


def format_datetime(value: datetime | None, language: str = "tr") -> str:
    if value is None:
        return "-"
    if language == "tr":
        return value.strftime("%d.%m.%Y %H:%M")
    return value.strftime("%Y-%m-%d %H:%M")


def data_delay_note(snapshot: StockSnapshot, language: str) -> str:
    key = "data_delay_realtime" if snapshot.realtime_enabled else "data_delay_delayed"
    return t(language, key)


def render_snapshot_message(
    snapshot: StockSnapshot,
    commentary_title: str,
    commentary: str,
    language: str,
) -> str:
    lines = [
        f"{snapshot.symbol} | {snapshot.company_name}",
        f"{t(language, 'last_price')}: {format_price(snapshot.last_price, language)} ({format_percent(snapshot.change_percent, language)})",
        f"{t(language, 'intraday_range')}: {format_price(snapshot.day_low, language)} - {format_price(snapshot.day_high, language)}",
        t(
            language,
            "open_volume",
            open_price=format_price(snapshot.open_price, language),
            volume=format_number(snapshot.volume, language),
        ),
        f"{t(language, 'monthly_change')}: {format_percent(snapshot.month_change_percent, language)}",
        f"{t(language, 'monthly_range')}: {format_price(snapshot.month_low, language)} - {format_price(snapshot.month_high, language)}",
        f"{t(language, 'market_cap')}: {format_compact_currency(snapshot.market_cap, language)}",
        t(
            language,
            "ratios",
            pe=format_numeric_ratio(snapshot.pe_ratio, language),
            pb=format_numeric_ratio(snapshot.pb_ratio, language),
        ),
        f"{t(language, 'year_range')}: {format_price(snapshot.year_low, language)} - {format_price(snapshot.year_high, language)}",
        t(
            language,
            "moving_averages",
            fifty=format_price(snapshot.fifty_day_average, language),
            two_hundred=format_price(snapshot.two_hundred_day_average, language),
        ),
        t(
            language,
            "ownership",
            foreign=format_percent(snapshot.foreign_ratio, language),
            free_float=format_percent(snapshot.free_float, language),
        ),
        f"{t(language, 'net_debt')}: {format_compact_currency(snapshot.net_debt, language)}",
        f"{t(language, 'updated_at')}: {format_datetime(snapshot.last_update, language)}",
        "",
        t(language, "financial_summary"),
        f"{t(language, 'revenue', year=snapshot.financial_year)}: {format_compact_currency(snapshot.revenue_latest, language)}",
        f"{t(language, 'revenue_change')}: {format_percent(snapshot.revenue_growth_percent, language)}",
        f"{t(language, 'gross_profit', year=snapshot.financial_year)}: {format_compact_currency(snapshot.gross_profit_latest, language)}",
        f"{t(language, 'net_income', year=snapshot.financial_year)}: {format_compact_currency(snapshot.net_income_latest, language)}",
        f"{t(language, 'operating_cashflow', year=snapshot.financial_year)}: {format_compact_currency(snapshot.operating_cashflow_latest, language)}",
    ]

    if snapshot.analyst_targets:
        lines.extend(
            [
                "",
                t(language, "analyst_summary"),
                f"{t(language, 'current_price')}: {format_price(to_float(snapshot.analyst_targets.get('current')), language)}",
                f"{t(language, 'mean_target')}: {format_price(to_float(snapshot.analyst_targets.get('mean')), language)}",
                f"{t(language, 'median_target')}: {format_price(to_float(snapshot.analyst_targets.get('median')), language)}",
                f"{t(language, 'target_range')}: {format_price(to_float(snapshot.analyst_targets.get('low')), language)} - {format_price(to_float(snapshot.analyst_targets.get('high')), language)}",
                f"{t(language, 'analyst_count')}: {format_number(to_float(snapshot.analyst_targets.get('numberOfAnalysts')), language)}",
            ]
        )

    if snapshot.recent_kap:
        lines.append("")
        lines.append(t(language, "recent_kap"))
        lines.extend(f"- {item}" for item in snapshot.recent_kap)

    if snapshot.upcoming_calendar:
        lines.append("")
        lines.append(t(language, "upcoming_calendar"))
        lines.extend(f"- {item}" for item in snapshot.upcoming_calendar)

    lines.extend(
        [
            "",
            f"{commentary_title}:",
            commentary.strip(),
            "",
            f"{t(language, 'note')}: {data_delay_note(snapshot, language)}",
            t(language, "disclaimer"),
        ]
    )

    return "\n".join(lines)

from __future__ import annotations

from openai import OpenAI

from bist_bot.company_context import get_company_context
from bist_bot.i18n import t
from bist_bot.stock_service import (
    StockSnapshot,
    data_delay_note,
    format_compact_currency,
    format_percent,
    format_price,
)


class AICommentaryService:
    def __init__(self, api_key: str | None, base_url: str, model: str) -> None:
        self._default_model = model
        self._client = OpenAI(api_key=api_key, base_url=base_url) if api_key else None

    def generate_commentary(
        self,
        snapshot: StockSnapshot,
        language: str,
        model: str | None = None,
    ) -> tuple[str, str]:
        if self._client is None:
            return t(language, "auto_commentary"), fallback_commentary(snapshot, language)

        active_model = model or self._default_model
        response = self._client.chat.completions.create(
            model=active_model,
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": build_system_prompt(language),
                },
                {
                    "role": "user",
                    "content": build_prompt(snapshot, language),
                },
            ],
        )

        message = response.choices[0].message.content or ""
        return t(language, "ai_commentary"), message.strip()


def build_system_prompt(language: str) -> str:
    if language == "en":
        return (
            "You are a neutral financial data commentator writing in English. "
            "Use only the provided numerical and corporate data. "
            "If company profile or contextual notes are provided, weave them into the analysis carefully. "
            "Do not invent market leadership claims that are not explicitly supplied. "
            "Do not give buy, sell, hold, target price, return promises, or investment advice. "
            "Do not predict prices. "
            "Write 5-7 concise professional sentences. "
            "Comment on company profile, operating performance, valuation ratios, financial momentum, and the tone of KAP disclosures. "
            "Naturally mention that some data may be delayed."
        )

    return (
        "Sen Turkce yazan tarafsiz bir finans veri yorumcususun. "
        "Sadece verilen sayisal ve kurumsal verilere dayan. "
        "Sirket profili veya baglamsal notlar verildiyse bunlari dikkatli sekilde kullan. "
        "Acikca verilmemis liderlik ya da pazar buyuklugu iddialari uydurma. "
        "Kesinlikle alim, satim, tut, hedef fiyat, kazanc vaadi veya yatirim tavsiyesi verme. "
        "Fiyat tahmini yapma. "
        "Kisa, net ve profesyonel bir dille 5-7 cumle kur. "
        "Sirketin ne is yaptigini, one cikan operasyonel tabloyu, degerleme carpanlarini, finansal ivmeyi ve KAP akisinin tonunu yorumla. "
        "Veri gecikmeli olabilecegini dogal sekilde belirt."
    )


def build_prompt(snapshot: StockSnapshot, language: str) -> str:
    kap_lines = "\n".join(f"- {item}" for item in snapshot.recent_kap) or "- N/A"
    calendar_lines = "\n".join(f"- {item}" for item in snapshot.upcoming_calendar) or "- N/A"
    context_notes = get_company_context(snapshot.symbol, language) or snapshot.context_notes
    context_lines = "\n".join(f"- {item}" for item in context_notes) or "- N/A"

    if language == "en":
        return f"""
Symbol: {snapshot.symbol}
Company: {snapshot.company_name}
Sector: {snapshot.sector}
Industry: {snapshot.industry}
Website: {snapshot.website}
Business summary: {snapshot.business_summary}
Company context notes:
{context_lines}
Last price: {format_price(snapshot.last_price, language)}
Daily change: {format_percent(snapshot.change_percent, language)}
1M change: {format_percent(snapshot.month_change_percent, language)}
Market cap: {format_compact_currency(snapshot.market_cap, language)}
P/E: {snapshot.pe_ratio}
P/B: {snapshot.pb_ratio}
52-week low-high: {format_price(snapshot.year_low, language)} / {format_price(snapshot.year_high, language)}
50-day average: {format_price(snapshot.fifty_day_average, language)}
200-day average: {format_price(snapshot.two_hundred_day_average, language)}
Foreign ratio: {format_percent(snapshot.foreign_ratio, language)}
Free float: {format_percent(snapshot.free_float, language)}
Net debt: {format_compact_currency(snapshot.net_debt, language)}
{snapshot.financial_year} revenue: {format_compact_currency(snapshot.revenue_latest, language)}
Revenue growth: {format_percent(snapshot.revenue_growth_percent, language)}
{snapshot.financial_year} gross profit: {format_compact_currency(snapshot.gross_profit_latest, language)}
{snapshot.financial_year} net income: {format_compact_currency(snapshot.net_income_latest, language)}
{snapshot.financial_year} operating cash flow: {format_compact_currency(snapshot.operating_cashflow_latest, language)}
Analyst target summary: {snapshot.analyst_targets}
Recent KAP disclosures:
{kap_lines}
Upcoming calendar:
{calendar_lines}
Data note: {data_delay_note(snapshot, language)}

Comment only on company data. Do not provide investment advice.
""".strip()

    return f"""
Sembol: {snapshot.symbol}
Sirket: {snapshot.company_name}
Sektor: {snapshot.sector}
Endustri: {snapshot.industry}
Web sitesi: {snapshot.website}
Faaliyet ozeti: {snapshot.business_summary}
Sirket baglam notlari:
{context_lines}
Son fiyat: {format_price(snapshot.last_price, language)}
Gunluk degisim: {format_percent(snapshot.change_percent, language)}
1 aylik degisim: {format_percent(snapshot.month_change_percent, language)}
Piyasa degeri: {format_compact_currency(snapshot.market_cap, language)}
F/K: {snapshot.pe_ratio}
PD/DD: {snapshot.pb_ratio}
52 hafta dusuk-yuksek: {format_price(snapshot.year_low, language)} / {format_price(snapshot.year_high, language)}
50 gun ortalama: {format_price(snapshot.fifty_day_average, language)}
200 gun ortalama: {format_price(snapshot.two_hundred_day_average, language)}
Yabanci orani: {format_percent(snapshot.foreign_ratio, language)}
Halka aciklik: {format_percent(snapshot.free_float, language)}
Net borc: {format_compact_currency(snapshot.net_debt, language)}
{snapshot.financial_year} satis geliri: {format_compact_currency(snapshot.revenue_latest, language)}
Satis buyumesi: {format_percent(snapshot.revenue_growth_percent, language)}
{snapshot.financial_year} brut kar: {format_compact_currency(snapshot.gross_profit_latest, language)}
{snapshot.financial_year} net donem kari: {format_compact_currency(snapshot.net_income_latest, language)}
{snapshot.financial_year} isletme nakit akisi: {format_compact_currency(snapshot.operating_cashflow_latest, language)}
Analist hedef ozeti: {snapshot.analyst_targets}
Son KAP bildirimleri:
{kap_lines}
Yaklasan takvim:
{calendar_lines}
Veri notu: {data_delay_note(snapshot, language)}

Yalnizca sirket verisini yorumla. Yatirim tavsiyesi verme.
""".strip()


def fallback_commentary(snapshot: StockSnapshot, language: str) -> str:
    if language == "en":
        return fallback_commentary_en(snapshot)
    return fallback_commentary_tr(snapshot)


def fallback_commentary_tr(snapshot: StockSnapshot) -> str:
    parts: list[str] = []
    context_notes = get_company_context(snapshot.symbol, "tr") or snapshot.context_notes
    if context_notes:
        parts.append(context_notes[0])
    elif snapshot.business_summary:
        parts.append(snapshot.business_summary)

    if snapshot.change_percent is not None and snapshot.month_change_percent is not None:
        parts.append(
            f"Hisse son islemde {format_price(snapshot.last_price, 'tr')} seviyesinde ve gunluk performansi {format_percent(snapshot.change_percent, 'tr')}, son bir aylik performansi ise {format_percent(snapshot.month_change_percent, 'tr')} duzeyinde gorunuyor."
        )
    elif snapshot.last_price is not None:
        parts.append(f"Hisse icin elde edilen son fiyat {format_price(snapshot.last_price, 'tr')} seviyesinde.")

    valuation_bits: list[str] = []
    if snapshot.pe_ratio is not None:
        valuation_bits.append(f"F/K oraninin {snapshot.pe_ratio:.2f} seviyesinde olmasi")
    if snapshot.pb_ratio is not None:
        valuation_bits.append(f"PD/DD oraninin {snapshot.pb_ratio:.2f} olarak izlenmesi")
    if valuation_bits:
        parts.append(", ".join(valuation_bits) + " sirketin borsa carpanlari acisindan izlenebilecek temel gostergelerden biri.")

    finance_bits: list[str] = []
    if snapshot.revenue_latest is not None:
        finance_bits.append(f"{snapshot.financial_year} satis geliri {format_compact_currency(snapshot.revenue_latest, 'tr')}")
    if snapshot.revenue_growth_percent is not None:
        finance_bits.append(f"yillik satis degisimi {format_percent(snapshot.revenue_growth_percent, 'tr')}")
    if snapshot.operating_cashflow_latest is not None:
        finance_bits.append(f"isletme nakit akisi {format_compact_currency(snapshot.operating_cashflow_latest, 'tr')}")
    if finance_bits:
        parts.append("Finansal tarafta " + ", ".join(finance_bits) + " olarak okunuyor.")

    if snapshot.recent_kap:
        parts.append(
            f"Son KAP akisinda one cikan baslik '{snapshot.recent_kap[0].split(': ', 1)[-1]}' oldu; bu nedenle kurumsal bildirim akisinin tonu da takibe deger."
        )

    parts.append(f"Veri notu olarak, {data_delay_note(snapshot, 'tr').lower()}")
    return " ".join(parts)


def fallback_commentary_en(snapshot: StockSnapshot) -> str:
    parts: list[str] = []
    context_notes = get_company_context(snapshot.symbol, "en") or snapshot.context_notes
    if context_notes:
        parts.append(context_notes[0])
    elif snapshot.business_summary:
        parts.append(snapshot.business_summary)

    if snapshot.change_percent is not None and snapshot.month_change_percent is not None:
        parts.append(
            f"The stock is currently around {format_price(snapshot.last_price, 'en')}, with a daily move of {format_percent(snapshot.change_percent, 'en')} and a one-month change of {format_percent(snapshot.month_change_percent, 'en')}."
        )
    elif snapshot.last_price is not None:
        parts.append(f"The latest observed price is {format_price(snapshot.last_price, 'en')}.")

    valuation_bits: list[str] = []
    if snapshot.pe_ratio is not None:
        valuation_bits.append(f"a P/E ratio of {snapshot.pe_ratio:.2f}")
    if snapshot.pb_ratio is not None:
        valuation_bits.append(f"a P/B ratio of {snapshot.pb_ratio:.2f}")
    if valuation_bits:
        parts.append("On valuation, " + " and ".join(valuation_bits) + " are key reference points.")

    finance_bits: list[str] = []
    if snapshot.revenue_latest is not None:
        finance_bits.append(f"{snapshot.financial_year} revenue of {format_compact_currency(snapshot.revenue_latest, 'en')}")
    if snapshot.revenue_growth_percent is not None:
        finance_bits.append(f"revenue change of {format_percent(snapshot.revenue_growth_percent, 'en')}")
    if snapshot.operating_cashflow_latest is not None:
        finance_bits.append(f"operating cash flow of {format_compact_currency(snapshot.operating_cashflow_latest, 'en')}")
    if finance_bits:
        parts.append("Financially, the latest picture shows " + ", ".join(finance_bits) + ".")

    if snapshot.recent_kap:
        parts.append(
            f"The most visible recent KAP headline was '{snapshot.recent_kap[0].split(': ', 1)[-1]}', so disclosure flow remains relevant for context."
        )

    parts.append("Data note: " + data_delay_note(snapshot, "en"))
    return " ".join(parts)

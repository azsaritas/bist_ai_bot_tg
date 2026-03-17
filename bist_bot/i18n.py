from __future__ import annotations

from typing import Any


SUPPORTED_LANGUAGES = ("tr", "en")
DEFAULT_LANGUAGE = "tr"
SUPPORTED_AI_MODELS = (
    "gemini-fast",
    "claude-airforce",
    "openai-fast",
    "perplexity-fast",
    "step-3.5-flash",
)

LANGUAGE_LABELS = {
    "tr": "Türkçe",
    "en": "English",
}

LANGUAGE_ALIASES = {
    "tr": {"tr", "turkish", "turkce", "türkçe", "turkçe"},
    "en": {"en", "english", "ingilizce"},
}

TRANSLATIONS = {
    "tr": {
        "select_language": "Lütfen bir dil seçin. / Please choose a language.",
        "language_changed": "Dil tercihiniz Türkçe olarak kaydedildi.",
        "language_required": "Devam etmek için önce bir dil seçin.",
        "choose_ai_model": "Lütfen bir AI modeli seçin.",
        "available_ai_models": "Mevcut seçenekler:",
        "current_ai_model": "Aktif AI modeli: {model}",
        "ai_model_changed": "AI modeli güncellendi: {model}",
        "invalid_ai_model": "Geçersiz model seçimi. Lütfen listeden bir model seçin.",
        "usage_stock": "Kullanım: /hisse THYAO",
        "usage_search": "Kullanım: /ara banka",
        "usage_aimodel": "Kullanım: /aimodel veya /aimodel gemini-fast",
        "found_companies": "Bulunan şirketler:",
        "no_match": "Eşleşen şirket bulunamadı.",
        "ambiguous_header": "Birden fazla şirket bulundu. Lütfen daha net yazın ya da hisse kodunu gönderin:",
        "company_not_found": "Şirket bulunamadı.",
        "empty_query": "Boş sorgu gönderildi.",
        "unexpected_error": "Bir hata oluştu. Lütfen biraz sonra tekrar deneyin.",
        "stock_unavailable": "Hisse verisi alınamadı. Kodun doğru olduğundan emin olup tekrar deneyin.",
        "start_intro": "{app_name}'a hoş geldin.",
        "start_body": "Bir hisse kodu ya da şirket adı gönderebilirsin.",
        "examples": "Örnekler:",
        "app_link": "Uygulama linki: {url}",
        "start_value": "Bu bot, güncel BIST verisini toplar ve Pollinations {model} modeliyle yatırım tavsiyesi içermeyen kısa bir yorum üretir.",
        "about_app": "Uygulama: {app_name}",
        "about_category": "Kategori: Telegram tabanlı BIST hisse analiz asistanı",
        "about_model": "Pollinations model: {model}",
        "about_api": "Pollinations API: {url}",
        "about_value": "Temel değer önerisi: BIST hisseleri için veri + yorum + KAP özeti",
        "about_language": "Uygulama dili: {lang_name}",
        "about_realtime": "Gerçek zaman modu: {status}",
        "realtime_on": "aktif",
        "realtime_off": "kapalı",
        "public_app_url": "Public app URL: {url}",
        "open_source_repo": "Open source repo: {url}",
        "discord": "Discord: {value}",
        "contact": "İletişim: {value}",
        "built_with": "Built with pollinations.ai",
        "submission_note": "README ve başvuru notları repoda Pollinations submission formatına göre düzenlenmiştir.",
        "last_price": "Son fiyat",
        "intraday_range": "Gün içi aralık",
        "open_volume": "Açılış: {open_price} | Hacim: {volume}",
        "monthly_change": "1 aylık değişim",
        "monthly_range": "1 aylık bant",
        "market_cap": "Piyasa değeri",
        "ratios": "F/K: {pe} | PD/DD: {pb}",
        "year_range": "52 hafta",
        "moving_averages": "50G HO: {fifty} | 200G HO: {two_hundred}",
        "ownership": "Yabancı oranı: {foreign} | Halka açıklık: {free_float}",
        "net_debt": "Net borç",
        "updated_at": "Güncelleme zamanı",
        "financial_summary": "Finansal özet:",
        "revenue": "{year} satış geliri",
        "revenue_change": "Yıllık satış değişimi",
        "gross_profit": "{year} brüt kar",
        "net_income": "{year} net dönem karı",
        "operating_cashflow": "{year} işletme nakit akışı",
        "analyst_summary": "Analist hedef özeti:",
        "current_price": "Mevcut fiyat",
        "mean_target": "Ortalama hedef",
        "median_target": "Medyan hedef",
        "target_range": "Hedef aralığı",
        "analyst_count": "Analist sayısı",
        "recent_kap": "Son KAP bildirimleri:",
        "upcoming_calendar": "Yaklaşan takvim:",
        "note": "Not",
        "disclaimer": "Bu içerik yatırım tavsiyesi değildir; yalnızca kamusal şirket verilerinin yorumsal bir özetidir.",
        "ai_commentary": "AI Yorumu",
        "auto_commentary": "Otomatik Yorum",
        "data_delay_realtime": "TradingView kimlik doğrulaması aktif; fiyatlar gerçek zamana daha yakın.",
        "data_delay_delayed": "TradingView oturumu tanımlı değil; fiyat verisi borsapy varsayılan akışı nedeniyle yaklaşık 15 dakika gecikmeli olabilir.",
    },
    "en": {
        "select_language": "Please choose a language. / Lütfen bir dil seçin.",
        "language_changed": "Your language preference has been saved as English.",
        "language_required": "Please choose a language before continuing.",
        "choose_ai_model": "Please choose an AI model.",
        "available_ai_models": "Available options:",
        "current_ai_model": "Active AI model: {model}",
        "ai_model_changed": "AI model updated: {model}",
        "invalid_ai_model": "Invalid model selection. Please choose a model from the list.",
        "usage_stock": "Usage: /stock THYAO or /hisse THYAO",
        "usage_search": "Usage: /search bank or /ara banka",
        "usage_aimodel": "Usage: /aimodel or /aimodel gemini-fast",
        "found_companies": "Matched companies:",
        "no_match": "No matching company was found.",
        "ambiguous_header": "Multiple companies matched. Please be more specific or send the ticker symbol:",
        "company_not_found": "Company not found.",
        "empty_query": "An empty query was sent.",
        "unexpected_error": "Something went wrong. Please try again in a moment.",
        "stock_unavailable": "Stock data could not be fetched. Please verify the symbol and try again.",
        "start_intro": "Welcome to {app_name}.",
        "start_body": "You can send a stock ticker or a company name.",
        "examples": "Examples:",
        "app_link": "App link: {url}",
        "start_value": "This bot collects current BIST market data and uses the Pollinations {model} model to produce a short non-investment commentary.",
        "about_app": "App: {app_name}",
        "about_category": "Category: Telegram-based BIST stock analysis assistant",
        "about_model": "Pollinations model: {model}",
        "about_api": "Pollinations API: {url}",
        "about_value": "Core value: BIST stock data + commentary + KAP summary",
        "about_language": "App language: {lang_name}",
        "about_realtime": "Realtime mode: {status}",
        "realtime_on": "enabled",
        "realtime_off": "disabled",
        "public_app_url": "Public app URL: {url}",
        "open_source_repo": "Open source repo: {url}",
        "discord": "Discord: {value}",
        "contact": "Contact: {value}",
        "built_with": "Built with pollinations.ai",
        "submission_note": "README and submission notes in the repo follow the Pollinations submission format.",
        "last_price": "Last price",
        "intraday_range": "Intraday range",
        "open_volume": "Open: {open_price} | Volume: {volume}",
        "monthly_change": "1M change",
        "monthly_range": "1M range",
        "market_cap": "Market cap",
        "ratios": "P/E: {pe} | P/B: {pb}",
        "year_range": "52-week range",
        "moving_averages": "50D MA: {fifty} | 200D MA: {two_hundred}",
        "ownership": "Foreign ratio: {foreign} | Free float: {free_float}",
        "net_debt": "Net debt",
        "updated_at": "Updated at",
        "financial_summary": "Financial summary:",
        "revenue": "{year} revenue",
        "revenue_change": "YoY revenue change",
        "gross_profit": "{year} gross profit",
        "net_income": "{year} net income",
        "operating_cashflow": "{year} operating cash flow",
        "analyst_summary": "Analyst target summary:",
        "current_price": "Current price",
        "mean_target": "Average target",
        "median_target": "Median target",
        "target_range": "Target range",
        "analyst_count": "Analyst count",
        "recent_kap": "Recent KAP disclosures:",
        "upcoming_calendar": "Upcoming calendar:",
        "note": "Note",
        "disclaimer": "This content is not investment advice; it is only an interpretive summary of public company data.",
        "ai_commentary": "AI Commentary",
        "auto_commentary": "Automatic Commentary",
        "data_delay_realtime": "TradingView authentication is active, so prices are closer to realtime.",
        "data_delay_delayed": "TradingView authentication is not configured, so price data may be delayed by about 15 minutes due to the default borsapy feed.",
    },
}


def t(language: str, key: str, **kwargs: Any) -> str:
    lang = language if language in TRANSLATIONS else DEFAULT_LANGUAGE
    template = TRANSLATIONS[lang][key]
    return template.format(**kwargs)


def language_name(language: str, ui_language: str) -> str:
    if ui_language == "tr":
        return "Türkçe" if language == "tr" else "İngilizce"
    return "Turkish" if language == "tr" else "English"


def parse_language_selection(text: str) -> str | None:
    normalized = (text or "").strip().lower()
    for language, labels in LANGUAGE_ALIASES.items():
        if normalized in labels or normalized == LANGUAGE_LABELS[language].lower():
            return language
    return None


def build_language_keyboard() -> dict[str, Any]:
    return {
        "keyboard": [
            [{"text": LANGUAGE_LABELS["tr"]}, {"text": LANGUAGE_LABELS["en"]}],
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True,
    }


def build_remove_keyboard() -> dict[str, Any]:
    return {"remove_keyboard": True}


def parse_ai_model_selection(text: str) -> str | None:
    normalized = (text or "").strip().lower()
    for model in SUPPORTED_AI_MODELS:
        if normalized == model.lower():
            return model
    return None


def build_ai_model_keyboard() -> dict[str, Any]:
    return {
        "keyboard": [
            [{"text": "gemini-fast"}, {"text": "claude-airforce"}],
            [{"text": "openai-fast"}, {"text": "perplexity-fast"}],
            [{"text": "step-3.5-flash"}],
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True,
    }

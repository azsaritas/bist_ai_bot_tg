from __future__ import annotations


COMPANY_CONTEXT: dict[str, dict[str, list[str]]] = {
    "THYAO": {
        "tr": [
            "Türkiye'nin bayrak taşıyıcı hava yolu şirketidir.",
            "Uluslararası yolcu trafiği ve dış hat ağı şirket hikayesinin önemli parçalarıdır.",
        ],
        "en": [
            "It is Turkey's flag carrier airline.",
            "International passenger traffic and the foreign route network are central parts of its story.",
        ],
    },
    "ASELS": {
        "tr": [
            "Türkiye savunma elektroniğinde öne çıkan şirketlerden biridir.",
            "Savunma sanayii projeleri ve kamu bağlantılı sipariş akışı temel hikayede önem taşır.",
        ],
        "en": [
            "It is one of the prominent companies in Turkey's defense electronics field.",
            "Defense industry projects and public-sector-linked order flow are important parts of the story.",
        ],
    },
    "TUPRS": {
        "tr": [
            "Türkiye rafineri tarafında belirleyici oyunculardan biridir.",
            "Enerji fiyatları, rafineri marjları ve iç talep görünümü şirket için kritik değişkenlerdir.",
        ],
        "en": [
            "It is one of the key players in Turkey's refining business.",
            "Energy prices, refinery margins, and domestic demand are critical variables for the company.",
        ],
    },
    "FROTO": {
        "tr": [
            "Türkiye'nin önde gelen otomotiv üreticileri arasında yer alır.",
            "Ticari araç üretimi ve ihracat performansı şirket anlatısında önemli yer tutar.",
        ],
        "en": [
            "It is among Turkey's leading automotive manufacturers.",
            "Commercial vehicle production and export performance are important parts of the company narrative.",
        ],
    },
    "SISE": {
        "tr": [
            "Düz cam, cam ambalaj ve kimyasallar tarafında yaygın faaliyet gösteren sanayi şirketidir.",
        ],
        "en": [
            "It is an industrial company active across flat glass, glass packaging, and chemicals.",
        ],
    },
    "BIMAS": {
        "tr": [
            "Organize gıda perakendesi tarafında geniş mağaza ağıyla bilinir.",
        ],
        "en": [
            "It is known for its wide store network in organized food retail.",
        ],
    },
    "KCHOL": {
        "tr": [
            "Türkiye'nin en büyük holding yapılarından biri olarak farklı sektörlere yayılmış iştiraklere sahiptir.",
        ],
        "en": [
            "As one of Turkey's largest holding structures, it has subsidiaries spread across multiple sectors.",
        ],
    },
    "SAHOL": {
        "tr": [
            "Holding yapısı nedeniyle banka, enerji, sanayi ve sigorta gibi alanlara yayılan bir portföye sahiptir.",
        ],
        "en": [
            "Its holding structure gives it exposure to banking, energy, industry, and insurance.",
        ],
    },
}


def get_company_context(symbol: str, language: str) -> list[str]:
    entry = COMPANY_CONTEXT.get(symbol.upper(), {})
    return entry.get(language) or entry.get("tr") or []

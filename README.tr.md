# BIST AI Telegram Bot

[![Built with Pollinations](https://img.shields.io/badge/Built%20with-Pollinations-8a2be2?style=for-the-badge)](https://pollinations.ai)

`BIST AI Telegram Bot`, Borsa Istanbul hisseleri için Telegram üzerinden veri özeti, KAP akışı ve yapay zeka destekli şirket yorumu sunan açık kaynaklı bir uygulamadır.

İngilizce sürüm: [README.md](/c:/Users/azsar/Desktop/bist-ai-bot-tg/README.md)

## Uygulama Özeti

- Uygulama adı: `BIST AI Telegram Bot`
- Uygulama tipi: Telegram yardımcı aracı / finans asistanı
- Ana değer önerisi: BIST hisseleri için veri toplama, şirket özeti, KAP akışı ve AI yorumu
- Pollinations kullanımı: `gemini-fast`, `claude-airforce`, `openai-fast`, `perplexity-fast` ve `step-3.5-flash` gibi modellerle yorum üretimi
- Uygulama bağlantısı: `https://t.me/<bot_username>` formatında yayınlanabilir
- Açık kaynak repo: bu repository

## Özellikler

- Hisse kodu veya şirket adıyla sorgu
- İlk açılışta Türkçe / English dil seçimi
- Sohbet bazlı `/aimodel` ile AI model seçimi
- Fiyat özeti, günlük değişim, hacim, çarpanlar ve 52 hafta bandı
- Ham teknik veri ötesinde temel analiz bağlamı
- Finansal tablo özeti
- Son KAP bildirimleri ve yaklaşan finansal takvim
- Pollinations destekli AI yorumu
- Pollinations API yoksa fallback yorum
- `/about` ile uygulama metadatası gösterimi

## Komutlar

- `/start`
- `/help`
- `/language`
- `/aimodel`
- `/about`
- `/pollinations`
- `/search bank`
- `/ara banka`
- `/stock THYAO`
- `/hisse THYAO`
- `THYAO`
- `Turk Hava Yollari`

## Desteklenen Pollinations Modelleri

Kullanıcılar `/aimodel` ile aktif metin modelini seçebilir.

- `gemini-fast`
- `claude-airforce`
- `openai-fast`
- `perplexity-fast`
- `step-3.5-flash`

## Pollinations Entegrasyonu

- Sağlayıcı: [pollinations.ai](https://pollinations.ai)
- Dokümantasyon: https://enter.pollinations.ai/api/docs
- LLM özeti: https://enter.pollinations.ai/api/docs/llm.txt
- API tipi: OpenAI uyumlu `/v1/chat/completions`
- Varsayılan model: `gemini-fast`

## Yerel Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

## Ortam Değişkenleri

Minimum gerekli alanlar:

```env
TELEGRAM_BOT_TOKEN=...
TELEGRAM_BOT_USERNAME=...
POLLINATIONS_API_KEY=...
POLLINATIONS_MODEL=gemini-fast
POLLINATIONS_BASE_URL=https://gen.pollinations.ai/v1
```

İsteğe bağlı olarak TradingView kimlik bilgileri tanımlanırsa fiyat verisi daha güncel hale getirilebilir.

## Kaynaklar

- Telegram Bot API: https://core.telegram.org/bots/api
- Pollinations API docs: https://enter.pollinations.ai/api/docs
- Pollinations submission template: https://github.com/pollinations/pollinations/issues/new?template=tier-app-submission.yml
- Pollinations contributing guide: https://github.com/pollinations/pollinations/blob/main/CONTRIBUTING.md
- Pollinations apps guide: https://github.com/pollinations/pollinations/blob/main/apps/README.md
- borsapy: https://github.com/saidsurucu/borsapy

# BIST AI Telegram Bot

[![Built with Pollinations](https://img.shields.io/badge/Built%20with-Pollinations-8a2be2?style=for-the-badge)](https://pollinations.ai)

`BIST AI Telegram Bot`, Borsa Istanbul hisseleri icin Telegram uzerinden veri ozeti, KAP akisi ve yapay zeka destekli sirket yorumu sunan acik kaynakli bir uygulamadir.


## App Summary

- App name: `BIST AI Telegram Bot`
- App type: Telegram utility / finance assistant
- Main user value: BIST hisseleri icin veri toplama + yorumlama + KAP ozeti
- Pollinations usage: `gemini-fast` text modeli ile yatirim tavsiyesi icermeyen Turkce yorum
- External app URL: `https://t.me/<bot_username>` formatinda kullanilabilir
- Open-source repo: bu repository

## Why This Fits Pollinations Better

Bu uygulama yalnizca "prompt gir, cevap al" tipinde ince bir sarmal degildir. Kullanicidan hisse kodu veya sirket adi alir, `borsapy` ile gercek veri toplar, finansal tablo ozetleri cikarir, son KAP bildirimlerini birlestirir ve bunlari Pollinations modeline anlamli bir baglam olarak verip kullaniciya duzenlenmis bir sirket yorumu sunar.

## Features

- Hisse kodu veya sirket adiyla sorgu
- Ilk acilista Turkce / English dil secimi
- Son fiyat, gunluk degisim, hacim, 52 hafta bandi ve temel carpanlar
- Finansal tablo ozeti
- Son KAP bildirimleri ve yaklasan finansal takvim
- Pollinations `gemini-fast` ile AI yorum
- `/aimodel` ile `gemini-fast`, `claude-airforce`, `openai-fast`, `perplexity-fast`, `step-3.5-flash` secimi
- Pollinations API yoksa fallback veri odakli yorum
- `/about` komutuyla app metadata gosterimi

## Commands

- `/start`
- `/help`
- `/language`
- `/aimodel`
- `/about`
- `/pollinations`
- `/ara banka`
- `/hisse THYAO`
- `THYAO`
- `Turk Hava Yollari`

## Pollinations Integration

- Provider: [pollinations.ai](https://pollinations.ai)
- Docs: https://enter.pollinations.ai/api/docs
- LLM summary: https://enter.pollinations.ai/api/docs/llm.txt
- Model: `gemini-fast`
- API style: OpenAI-compatible `/v1/chat/completions`

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

## Environment Variables

Minimum gerekli alanlar:

```env
TELEGRAM_BOT_TOKEN=...
TELEGRAM_BOT_USERNAME=...
POLLINATIONS_API_KEY=...
POLLINATIONS_MODEL=gemini-fast
POLLINATIONS_BASE_URL=https://gen.pollinations.ai/v1
```

Submission-ready metadata alanlari:

```env
APP_NAME=BIST AI Telegram Bot
APP_PUBLIC_URL=https://t.me/<bot_username>
GITHUB_REPO_URL=https://github.com/<username>/<repo>
APP_LANGUAGE=tr
DISCORD_CONTACT=
OTHER_CONTACT=
```

Opsiyonel TradingView alanlari tanimlanirsa fiyat akisi daha guncel hale getirilebilir.

## Sources

- Telegram Bot API: https://core.telegram.org/bots/api
- Pollinations API docs: https://enter.pollinations.ai/api/docs
- Pollinations submission template: https://github.com/pollinations/pollinations/issues/new?template=tier-app-submission.yml
- Pollinations contributing guide: https://github.com/pollinations/pollinations/blob/main/CONTRIBUTING.md
- Pollinations apps guide: https://github.com/pollinations/pollinations/blob/main/apps/README.md
- borsapy: https://github.com/saidsurucu/borsapy

# BIST AI Telegram Bot

[![Built with Pollinations](https://img.shields.io/badge/Built%20with-Pollinations-8a2be2?style=for-the-badge)](https://pollinations.ai)

Open-source Telegram bot for Borsa Istanbul stock analysis with Pollinations-powered AI commentary.

Turkish version: [README.tr.md](/c:/Users/azsar/Desktop/bist-ai-bot-tg/README.tr.md)

## App Summary

- App name: `BIST AI Telegram Bot`
- App type: Telegram utility / finance assistant
- Main user value: BIST stock data, company summary, KAP flow, and AI commentary in one place
- Pollinations usage: text commentary generated through Pollinations models such as `gemini-fast`, `claude-airforce`, `openai-fast`, `perplexity-fast`, and `step-3.5-flash`
- External app URL: can be exposed as `https://t.me/<bot_username>`
- Open-source repo: this repository

## Features

- Search by stock ticker or company name
- First-run language selection with Turkish and English support
- Per-chat AI model selection with `/aimodel`
- Price summary, daily move, volume, valuation ratios, and 52-week range
- Basic fundamental-analysis context beyond raw technical data
- Financial statement summary
- Recent KAP disclosures and upcoming reporting calendar
- Pollinations-powered AI commentary
- Fallback commentary when Pollinations API is unavailable
- `/about` command for app metadata and submission-friendly details

## Commands

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

## Supported Pollinations Models

Users can choose the active text model with `/aimodel`.

- `gemini-fast`
- `claude-airforce`
- `openai-fast`
- `perplexity-fast`
- `step-3.5-flash`

## Pollinations Integration

- Provider: [pollinations.ai](https://pollinations.ai)
- Docs: https://enter.pollinations.ai/api/docs
- LLM summary: https://enter.pollinations.ai/api/docs/llm.txt
- API style: OpenAI-compatible `/v1/chat/completions`
- Default model: `gemini-fast`

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

## Environment Variables

Minimum required:

```env
TELEGRAM_BOT_TOKEN=...
TELEGRAM_BOT_USERNAME=...
POLLINATIONS_API_KEY=...
POLLINATIONS_MODEL=gemini-fast
POLLINATIONS_BASE_URL=https://gen.pollinations.ai/v1
```

Optional TradingView credentials can be configured for fresher pricing data.


## Sources

- Telegram Bot API: https://core.telegram.org/bots/api
- Pollinations API docs: https://enter.pollinations.ai/api/docs
- Pollinations submission template: https://github.com/pollinations/pollinations/issues/new?template=tier-app-submission.yml
- Pollinations contributing guide: https://github.com/pollinations/pollinations/blob/main/CONTRIBUTING.md
- Pollinations apps guide: https://github.com/pollinations/pollinations/blob/main/apps/README.md
- borsapy: https://github.com/saidsurucu/borsapy

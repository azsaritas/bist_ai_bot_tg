# Deployment Guide

This bot does not expose an HTTP port. It runs as a background worker and polls Telegram continuously.

## Recommended Setup

Run it as a separate Docker container next to your existing Python service.

## 1. Copy the project to the server

Example:

```bash
git clone https://github.com/<username>/<repo>.git
cd <repo>
```

## 2. Create the environment file

```bash
cp .env.example .env
```

Fill in at least:

```env
TELEGRAM_BOT_TOKEN=...
TELEGRAM_BOT_USERNAME=...
POLLINATIONS_API_KEY=...
POLLINATIONS_MODEL=gemini-fast
POLLINATIONS_BASE_URL=https://gen.pollinations.ai/v1
```

Optional:

```env
TRADINGVIEW_USERNAME=
TRADINGVIEW_PASSWORD=
TRADINGVIEW_SESSION=
TRADINGVIEW_SESSION_SIGN=
```

## 3. Run as a standalone container

```bash
docker compose -f docker-compose.bot.yml up -d --build
```

Check logs:

```bash
docker compose -f docker-compose.bot.yml logs -f
```

Stop:

```bash
docker compose -f docker-compose.bot.yml down
```

## 4. Add it to an existing docker-compose stack

If your server already has another Python app running with Docker Compose, add this service to the existing `docker-compose.yml`:

```yaml
services:
  bist-ai-bot:
    build:
      context: /path/to/bist-ai-bot-tg
    container_name: bist-ai-bot
    restart: unless-stopped
    env_file:
      - /path/to/bist-ai-bot-tg/.env
    volumes:
      - /path/to/bist-ai-bot-tg/data:/app/data
```

Then run:

```bash
docker compose up -d --build bist-ai-bot
```

## Notes

- No port mapping is needed because the bot uses Telegram long polling.
- `./data:/app/data` keeps language and AI model selections persistent.
- `restart: unless-stopped` makes the bot come back automatically after server restarts.
- Keep `.env` on the server and do not commit it to Git.

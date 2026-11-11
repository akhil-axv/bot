# Gemini Telegram Bot

A Telegram bot that uses Google's Gemini API to answer text messages and describe images.

## Features

- Responds to text messages with Gemini.
- Accepts image messages with an optional caption.
- Uses environment variables for credentials.
- Logs diagnostic details without returning raw exception text to users.

## Requirements

- Python 3.10 or newer
- A Telegram bot token
- A Google Gemini API key

## Setup

1. Create and activate a virtual environment.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and fill in fresh credentials.
4. Export the variables before starting the application:

```bash
set -a
. ./.env
set +a
python bot.py
```

Do not commit `.env` or paste credentials into source code. Rotate any token or API key that was previously committed.

## Project structure

- `bot.py`: Telegram handlers and Gemini integration
- `requirements.txt`: Python dependencies
- `.env.example`: names of required environment variables

## Responsible use

Respect Telegram and Google service terms, user privacy, and applicable laws. Avoid sending sensitive personal information to the bot.

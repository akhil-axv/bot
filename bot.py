import logging
import os

from google import genai
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

ai_client = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "Assalawma aleykum! Men Gemini AI botpan. "
            "Maǵan tekst jiberiń yamasa súwretke soraw qosıń."
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing",
    )
    try:
        response = await ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=update.message.text,
        )
        await update.message.reply_text(
            response.text or "AI bos juwap qaytardı. Qayta urınıp kóriń."
        )
    except Exception:
        logger.exception("Gemini text request failed")
        await update.message.reply_text(
            "Keshiriń, sorawıńızdı islewde qatelik júz berdi."
        )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.photo:
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing",
    )
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        caption = update.message.caption or "Bul súwretti qısqasha súwretlep beriń."
        response = await ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                genai.types.Part.from_bytes(
                    data=bytes(photo_bytes),
                    mime_type="image/jpeg",
                ),
                caption,
            ],
        )
        await update.message.reply_text(
            response.text or "Súwret boyınsha juwap alınbadı."
        )
    except Exception:
        logger.exception("Gemini image request failed")
        await update.message.reply_text(
            "Keshiriń, súwretti islewde qatelik júz berdi."
        )


def main() -> None:
    global ai_client

    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    missing = [
        name
        for name, value in (
            ("TELEGRAM_BOT_TOKEN", telegram_token),
            ("GEMINI_API_KEY", gemini_api_key),
        )
        if not value
    ]
    if missing:
        raise SystemExit(
            "Missing environment variable(s): " + ", ".join(missing)
        )

    ai_client = genai.Client(api_key=gemini_api_key).aio
    application = Application.builder().token(telegram_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    logger.info("Telegram bot is starting")
    application.run_polling()


if __name__ == "__main__":
    main()

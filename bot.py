import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# --- SAZLAMALAR ---
TELEGRAM_TOKEN = "8408293472:AAEn5Zk_AdBjnbitYtPlqdTxoOSCLXXwnp8"
GEMINI_API_KEY = "AIzaSyAQl8M4FXs4uBuxklHh45w1T7CAnzU51xU"

# Gemini klientin jana SDK arqali iske túsiremiz
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# Terminalda qatelerdi hám processti kóriw ushın logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start komandası kelgende bot beretuǵın juap
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Assalawma áleykum! Men Gemini 2.5 Flash penen isleytuǵın intellektual botpan. "
        "Maǵan qálegen sorawıńızdı jazıń yamasa súvret jiberiń, juap beriwge háreket etemen!"
    )

# Ápiwayı tekstli xabarlar kelgende isleytuǵın funkciya
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    
    # Bot "jazıpatır..." jaǵdayında turıwı ushın (typing indicator)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Gemini 2.5 modeline tekstti jiberemiz
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Gemini API qatelligi: {e}")
        await update.message.reply_text("Keshiriń, sorawıńızdı qayta islewde qatelik júz berdi.")

# Súvret jiberilgende isleytuǵın funkciya (Multimodal)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photo_file = await update.message.photo[-1].get_file()
    user_caption = update.message.caption if update.message.caption else "Ushı súvretti tolıq táriplep ber."
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        photo_bytes = await photo_file.download_as_bytearray()
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                genai.types.Part.from_bytes(
                    data=bytes(photo_bytes),
                    mime_type="image/jpeg"
                ),
                user_caption
            ]
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Súvret penen islesiwde qatelik: {e}")
        await update.message.reply_text("Keshiriń, súvretti oqıwda mashqala payda boldı.")

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot iske túsipatır... Toqtatıw ushın Ctrl+C basıń.")
    application.run_polling()

if __name__ == "__main__":
    main()


import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_NAME = os.getenv("BOT_NAME", "Glitcherion")
OWNER_ID = os.getenv("OWNER_ID", "000000")

application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(">> Comando /start recibido.")
    await update.message.reply_text(f"✨ Saludos, Amanda. Yo soy {BOT_NAME}, viajero de códigos rotos y sueños imposibles.")

application.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    logging.info(">> Iniciando Glitcherion en modo polling...")
    application.run_polling()


import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request
import logging
import asyncio

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_NAME = os.getenv("BOT_NAME", "Glitcherion")
OWNER_ID = os.getenv("OWNER_ID", "000000")

application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(">> Comando /start recibido.")
    await update.message.reply_text(f"✨ Saludos, Amanda. Yo soy {BOT_NAME}, viajero de códigos rotos y sueños imposibles.")

application.add_handler(CommandHandler("start", start))

web_app = Flask(__name__)

@web_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    logging.info(">> Webhook recibido por Flask.")
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

@web_app.route("/")
def home():
    return f"{BOT_NAME} está orbitando... 🚀"

if __name__ == "__main__":
    logging.info(">> Ejecutando Flask + Telegram sin threading.")
    application.initialize()
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

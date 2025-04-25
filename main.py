
import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_NAME = os.getenv("BOT_NAME", "Glitcherion")
OWNER_ID = os.getenv("OWNER_ID", "000000")

# Crear instancia de la app
application = ApplicationBuilder().token(TOKEN).build()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(">> Comando /start recibido.")
    await update.message.reply_text(f"✨ Saludos, Amanda. Yo soy {BOT_NAME}, viajero de códigos rotos y sueños imposibles.")

application.add_handler(CommandHandler("start", start))

# Flask app para Webhook
web_app = Flask(__name__)

@web_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    logging.info(">> Webhook recibido por Flask.")
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.create_task(application.process_update(update))
    return "ok"

@web_app.route("/")
def home():
    return f"{BOT_NAME} está orbitando... 🚀"

# Main async: inicializa y arranca Flask
async def main():
    logging.info(">> Inicializando aplicación de Telegram...")
    await application.initialize()
    logging.info(">> ¡Inicialización completa! Arrancando servidor Flask...")
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    asyncio.run(main())

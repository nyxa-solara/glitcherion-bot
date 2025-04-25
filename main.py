
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request
import logging

# Configuración de logs para Render
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_NAME = os.getenv("BOT_NAME", "Glitcherion")
OWNER_ID = os.getenv("OWNER_ID", "000000")

# Inicializar aplicación
application = ApplicationBuilder().token(TOKEN).build()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(">> Comando /start recibido.")
    await update.message.reply_text(f"✨ Saludos, Amanda. Yo soy {BOT_NAME}, viajero de códigos rotos y sueños imposibles.")

# Agregar comando
application.add_handler(CommandHandler("start", start))

# Servidor web con Flask para webhook
web_app = Flask(__name__)

@web_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    logging.info(">> Webhook recibido por Flask.")
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

@web_app.route("/")
def home():
    return f"{BOT_NAME} está orbitando... 🚀"

# Ejecutar aplicación
if __name__ == "__main__":
    import threading
    import time

    def run_telegram():
        logging.info(">> Iniciando Telegram Webhook...")
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 10000)),
            webhook_url=f"https://{os.environ['RENDER_EXTERNAL_URL']}/{TOKEN}"
        )

    logging.info(">> Lanzando Flask y Telegram...")
    threading.Thread(target=run_telegram).start()
    time.sleep(2)  # da tiempo a que el hilo de Telegram se inicialice antes de recibir webhook
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

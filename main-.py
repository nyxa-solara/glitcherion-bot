
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request

TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_NAME = os.getenv("BOT_NAME", "Glitcherion")
OWNER_ID = os.getenv("OWNER_ID", "000000")

application = ApplicationBuilder().token(TOKEN).build()

# Comando de inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(">> Comando /start recibido.")
    await update.message.reply_text(f"✨ Saludos, Amanda. Yo soy {BOT_NAME}, viajero de códigos rotos y sueños imposibles.")

application.add_handler(CommandHandler("start", start))

# Crear servidor Flask
web_app = Flask(__name__)

@web_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    print(">> Webhook recibido en Flask.")
    application.update_queue.put_nowait(Update.de_json(request.get_json(force=True), application.bot))
    return "ok"

@web_app.route("/")
def home():
    return f"{BOT_NAME} está orbitando... 🚀"

# Iniciar Telegram en un hilo separado y Flask principal
if __name__ == "__main__":
    import threading

    def run_telegram():
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 10000)),
            webhook_url=f"https://{os.environ['RENDER_EXTERNAL_URL']}/{TOKEN}"  # barra corregida aquí
        )

    threading.Thread(target=run_telegram).start()
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

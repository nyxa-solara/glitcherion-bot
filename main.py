import os
import random
import logging
import asyncio
import httpx
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Flask app para mantener Replit despierto
app = Flask(__name__)

@app.route('/')
def home():
    return "Glitcherion alive"

def run_flask():
    app.run(host='0.0.0.0', port=3000)

# Configuraciones
TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_NAME = os.getenv("BOT_NAME", "Glitcherion")
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")

# Estados de conversación
ASK_ORIGIN = range(1)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mensajes especiales aleatorios para glitches
GLITCH_MESSAGES = [
    "⚡️ *¡GLITCH DETECTADO EN LA MATRIX!* Aprovecha este portal absurdo antes que colapse.",
    "🚀 *¡El Viento Solar sopla a tu favor!* ¡Esta oferta es un llamado al salto cuántico!",
    "🛸 *¡Falla en la simulación!* Precios rotos, destinos abiertos. ¿Te atreves?",
    "🔮 *Un oráculo susurra:* 'El viajero audaz tomará esta senda improbable...'",
    "🔥 *¡PORTAL TEMPORAL ABIERTO!* Corre antes que las coordenadas se evaporen."
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"✨ Saludos, {update.effective_user.first_name}. Yo soy {BOT_NAME}, viajero de códigos rotos y sueños imposibles.")

async def vuelos_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛫 ¿Desde qué ciudad quieres partir? (Ej: ASU, GRU, EZE)")
    return ASK_ORIGIN

async def recibir_origen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from_airport = update.message.text.strip().upper()
    await buscar_vuelos(update, context, from_airport)
    return ConversationHandler.END

async def buscar_vuelos(update: Update, context: ContextTypes.DEFAULT_TYPE, from_airport: str):
    try:
        async with httpx.AsyncClient() as client:
            auth = await client.post(
                'https://test.api.amadeus.com/v1/security/oauth2/token',
                data={
                    'grant_type': 'client_credentials',
                    'client_id': AMADEUS_CLIENT_ID,
                    'client_secret': AMADEUS_CLIENT_SECRET
                }
            )
            token = auth.json().get('access_token')

            headers = {'Authorization': f'Bearer {token}'}
            params = {
                'originLocationCode': from_airport,
                'destinationLocationCode': 'BCN',  # Puede cambiarse luego
                'departureDate': '2025-05-10',      # Fecha dummy
                'adults': 1,
                'max': 3
            }
            vuelos = await client.get('https://test.api.amadeus.com/v2/shopping/flight-offers', headers=headers, params=params)
            resultados = vuelos.json()

            if 'data' not in resultados:
                await update.message.reply_text("🚫 No encontré vuelos desde ese aeropuerto.")
                return

            for vuelo in resultados['data']:
                precio = float(vuelo['price']['total'])
                origen = vuelo['itineraries'][0]['segments'][0]['departure']['iataCode']
                destino = vuelo['itineraries'][0]['segments'][-1]['arrival']['iataCode']
                fecha = vuelo['itineraries'][0]['segments'][0]['departure']['at']

                mensaje = f"\n🛫 {origen} → 🛬 {destino}\n📅 Fecha: {fecha}\n💵 Precio: USD {precio:.2f}"

                if precio < 100:
                    mensaje_especial = random.choice(GLITCH_MESSAGES)
                    mensaje = mensaje_especial + "\n" + mensaje

                await update.message.reply_text(mensaje)

    except Exception as e:
        logger.error(f"Error buscando vuelos: {e}")
        await update.message.reply_text("❌ Ocurrió un error buscando vuelos. Intenta más tarde.")

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operación cancelada.")
    return ConversationHandler.END

async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("vuelos", vuelos_start)],
        states={
            ASK_ORIGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_origen)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    thread = Thread(target=run_flask)
    thread.start()

    await application.run_polling()

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())

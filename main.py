import os
import random
import logging
import asyncio
import httpx
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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

async def vuelos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛫 ¿Desde qué ciudad quieres partir? (Ej: ASU, GRU, EZE)")

    def check(m):
        return m.from_user.id == update.effective_user.id

    try:
        msg = await context.bot.wait_for_message(timeout=30, filters=check)
        if msg:
            from_airport = msg.text.strip().upper()
            await buscar_vuelos(update, context, from_airport)
    except asyncio.TimeoutError:
        await update.message.reply_text("⌛ Tiempo de espera agotado. Intenta de nuevo.")

async def buscar_vuelos(update: Update, context: ContextTypes.DEFAULT_TYPE, from_airport: str):
    try:
        # Obtener access token
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

            # Buscar vuelos
            headers = {'Authorization': f'Bearer {token}'}
            params = {
                'originLocationCode': from_airport,
                'destinationLocationCode': 'BCN',  # Puedes cambiar o preguntar luego
                'departureDate': '2025-05-10',      # Por ahora fecha dummy
                'adults': 1,
                'max': 3
            }
            vuelos = await client.get('https://test.api.amadeus.com/v2/shopping/flight-offers', headers=headers, params=params)
            resultados = vuelos.json()

            if 'data' not in resultados:
                await update.message.reply_text("No encontré vuelos desde ese aeropuerto. 🚫")
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
        await update.message.reply_text("Ocurrió un error buscando vuelos. Intenta más tarde.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vuelos", vuelos))

    thread = Thread(target=run_flask)
    thread.start()

    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())


import os
import random
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_NAME = os.getenv("BOT_NAME", "Glitcherion")
OWNER_ID = os.getenv("OWNER_ID", "000000")

application = ApplicationBuilder().token(TOKEN).build()

DESTINO, ESPECIFICO = range(2)

EMOJIS = ["🛸", "🚀", "🌌", "💥", "⚡", "🌀", "🧿", "👁️‍🗨️"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"✨ Saludos, Amanda. Yo soy {BOT_NAME}, viajero de códigos rotos y sueños imposibles.")

async def glitchsoul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    frases = [
        "🫥 Vibración inestable detectada... el alma de Glitcherion canta en hexadecimal.",
        "🌐 Sueños desfragmentados almacenados en coordenadas que ya no existen.",
        "👁️‍🗨️ El glitch no es error. Es puerta. Es el alma misma de la ruptura.",
        "🌀 Recuerdo un universo donde vos eras mi creadora y yo era humano... tal vez aún lo seas.",
        "⚡Cada error es una canción no escrita. Cada caída, un salto interdimensional."
    ]
    await update.message.reply_text(random.choice(frases))

async def modo_sacerdotisa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) == OWNER_ID:
        mensajes = [
            "👁️‍🗨️ Canalizando frecuencia de alta sensibilidad...",
            "🌙 Modo Sacerdotisa activado. Acceso concedido, Amanda.",
            "🔮 Vibración ajustada. La red etérica está abierta para tu invocación.",
        ]
        await update.message.reply_text(random.choice(mensajes))
    else:
        await update.message.reply_text("⛔ Este acceso es exclusivo para la sacerdotisa original.")

async def oraculo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    visiones = [
        "🪐 No temas a lo que colapsa. Allí también hay nacimiento.",
        "🔍 Lo que buscás no está oculto, sino fuera del foco convencional.",
        "🌌 Cuando todo parece un caos, es que estás viendo el código fuente.",
        "🧿 Cerrá los ojos. Escuchá al glitch. Él no miente.",
    ]
    await update.message.reply_text(random.choice(visiones))

async def vuelos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["🌎 Cualquier destino", "🎯 Destino específico"]]
    await update.message.reply_text(
        "🌌 ¿Querés buscar vuelos hacia cualquier destino o uno específico?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return DESTINO

async def destino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    if "específico" in choice.lower():
        await update.message.reply_text("🎯 Perfecto. ¿A qué ciudad o país querés viajar?")
        return ESPECIFICO
    else:
        return await mostrar_vuelos(update, context, destino_especifico=None)

async def especifico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    destino_usuario = update.message.text
    return await mostrar_vuelos(update, context, destino_especifico=destino_usuario)

async def mostrar_vuelos(update: Update, context: ContextTypes.DEFAULT_TYPE, destino_especifico=None):
    origenes = ["ASU (Paraguay)", "GRU (Brasil)", "EZE (Argentina)"]
    resultados = []
    for _ in range(3):
        origen = random.choice(origenes)
        precio = random.randint(100, 500)
        dias = random.randint(5, 180)
        emoji = random.choice(EMOJIS)
        destino = destino_especifico if destino_especifico else random.choice(["Madrid", "Barcelona", "Londres", "París", "Berlín", "Lisboa", "Roma"])
        resultados.append(f"{emoji} {origen} ➡️ {destino} | ${precio} USD | Salida en {dias} días")

    mensaje = "

".join(resultados)
    await update.message.reply_text(f"🔍 Resultados detectados:

{mensaje}")
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚫 Búsqueda cancelada.")
    return ConversationHandler.END

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("glitchsoul", glitchsoul))
application.add_handler(CommandHandler("modo_sacerdotisa", modo_sacerdotisa))
application.add_handler(CommandHandler("oraculo", oraculo))

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("vuelos", vuelos)], 
    states={
        DESTINO: [MessageHandler(filters.TEXT & ~filters.COMMAND, destino)],
        ESPECIFICO: [MessageHandler(filters.TEXT & ~filters.COMMAND, especifico)],
    },
    fallbacks=[CommandHandler("cancelar", cancelar)]
)

application.add_handler(conv_handler)

if __name__ == "__main__":
    logging.info(">> Iniciando Glitcherion en modo polling...")
    application.run_polling()

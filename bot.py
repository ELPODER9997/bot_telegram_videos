import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configurar logging para ver errores
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Leer variables de entorno
TOKEN = os.environ.get("BOT_TOKEN", "")
GRUPO_ID_STR = os.environ.get("GRUPO_ID", "")

print(f"TOKEN recibido: {'SÍ' if TOKEN else 'NO'}")
print(f"GRUPO_ID recibido: {GRUPO_ID_STR}")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN no está configurado. Ve a Railway → Variables.")
if not GRUPO_ID_STR:
    raise ValueError("❌ GRUPO_ID no está configurado. Ve a Railway → Variables.")

GRUPO_ID = int(GRUPO_ID_STR)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Envíame un video y lo reenviaré al grupo privado.")

async def recibir_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = update.message.from_user
    nombre = usuario.full_name
    username = f"@{usuario.username}" if usuario.username else "sin username"
    
    try:
        if update.message.video:
            await context.bot.send_video(
                chat_id=GRUPO_ID,
                video=update.message.video.file_id,
                caption=f"📹 Video de: {nombre} ({username})"
            )
            await update.message.reply_text("✅ ¡Video enviado al grupo privado!")
        
        elif update.message.document and 'video' in (update.message.document.mime_type or ''):
            await context.bot.send_document(
                chat_id=GRUPO_ID,
                document=update.message.document.file_id,
                caption=f"📁 Archivo de video de: {nombre} ({username})"
            )
            await update.message.reply_text("✅ ¡Archivo de video enviado al grupo privado!")
        
        else:
            await update.message.reply_text("⚠️ Por favor, envía solo videos.")
            
    except Exception as error:
        await update.message.reply_text("❌ Hubo un error.")
        print(f"Error: {error}")

def main():
    # Crear aplicación
    application = Application.builder().token(TOKEN).build()
    
    # Añadir handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, recibir_video))
    
    print(f"🤖 Bot iniciado en Railway!")
    print(f"✅ GRUPO_ID configurado: {GRUPO_ID}")
    
    # Iniciar polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

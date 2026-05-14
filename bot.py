import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Lee variables con verificación
TOKEN = os.environ.get("BOT_TOKEN", "")
GRUPO_ID_STR = os.environ.get("GRUPO_ID", "")

# Depuración: imprimir valores para ver qué llega
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

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, recibir_video))
    
    print(f"🤖 Bot iniciado en Railway!")
    print(f"✅ GRUPO_ID configurado: {GRUPO_ID}")
    await app.run_polling()

if _name_ == "_main_":
    import asyncio
    asyncio.run(main())
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Lee las variables desde Railway (más seguro)
TOKEN = os.environ.get("BOT_TOKEN")
GRUPO_ID = int(os.environ.get("GRUPO_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! Envíame un video y lo reenviaré automáticamente al grupo privado."
    )

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
    
    print("🤖 Bot iniciado en Railway!")
    await app.run_polling()

if _name_ == "_main_":
    import asyncio
    asyncio.run(main())
import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "8083805550:AAFMBT1GbV0MJCYU7JQeuOx3D3umapjbx2w"

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Envie um link de vídeo para baixar!")

async def download_video(url):
    output_path = "downloads/%(title)s.%(ext)s"
    ydl_opts = {'outtmpl': output_path, 'format': 'best'}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    await update.message.reply_text("Baixando o vídeo, aguarde...")
    
    try:
        file_path = await download_video(url)
        await update.message.reply_video(video=open(file_path, "rb"))
        os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"Erro ao baixar o vídeo: {e}")
        return

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    main()
    
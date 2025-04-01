import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Get token from Railway environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Send /mp3 [URL] to download audio\n"
        "🎥 Send /mp4 [URL] to download video"
    )

# Download MP3
async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = update.message.text.split()[1]
        await update.message.reply_text("⏳ Downloading audio...")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3")
            await update.message.reply_audio(audio=open(filename, 'rb'))
            os.remove(filename)  # Delete file after sending

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# Download MP4
async def mp4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = update.message.text.split()[1]
        await update.message.reply_text("⏳ Downloading video...")

        ydl_opts = {
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            await update.message.reply_video(video=open(filename, 'rb'))
            os.remove(filename)  # Delete file after sending

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# Run bot
if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mp3", mp3))
    app.add_handler(CommandHandler("mp4", mp4))
    app.run_polling()
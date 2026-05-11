from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 تم استلام الصورة")

    await update.message.reply_text("""
🦂 جاري التعرف على النوع...

⚠️ هذا البوت للتوعية فقط
🚑 عند الإصابة توجه للطوارئ
""")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Bot Started...")

app.run_polling()

import os
import base64
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 تم استلام الصورة... جاري التحليل")

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_bytes = await file.download_as_bytearray()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
أنت مساعد توعوي للتعرف المبدئي على الثعابين والعقارب في السودان.

حلل الصورة وارجع الرد بالعربية بهذا الشكل:

1. النوع المتوقع:
2. مستوى الخطورة:
3. هل يبدو عقربًا أم ثعبانًا؟
4. علامات مميزة من الصورة:
5. إرشادات فورية:
6. تنبيه طبي:

مهم جدًا:
- لا تؤكد التشخيص.
- قل دائمًا إن النتيجة تقديرية.
- لا تصف أدوية.
- عند اللدغ أو الاشتباه، وجّه للطوارئ فورًا.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=600,
        )

        answer = response.choices[0].message.content

        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(
            "حدث خطأ أثناء التحليل. حاول مرة أخرى لاحقًا.\n\n"
            "⚠️ عند الإصابة أو الاشتباه باللدغ، توجه للطوارئ فورًا."
        )
        print("ERROR:", e)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Bot Started...")
app.run_polling()

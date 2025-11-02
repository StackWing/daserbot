import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from openai import OpenAI
import logging
import os

logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not OPENAI_API_KEY or not TELEGRAM_TOKEN:
    raise RuntimeError("❌ OPENAI_API_KEY կամ TELEGRAM_TOKEN միջավայրում չկան։")

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update, context):
    await update.message.reply_text("👋 Բարև, ես SmartEduBot-ն եմ։ Ուղարկիր հարց, և ես կօգնեմ։")


async def handle_message(update, context):
    prompt = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Դու կրթական օգնական ես։ Պատասխանիր հակիրճ և ճիշտ։"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        answer = response.choices[0].message.content.strip()
        await update.message.reply_text(answer)
    except Exception as e:
        logging.error(f"❌ OPENAI ERROR: {e}")
        await update.message.reply_text("⚠️ Սխալ տեղի ունեցավ։ Փորձիր կրկին։")


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("🤖 SmartEduBot is running...")
    app.run_polling()  # ✅ Նոր տարբերակի ճիշտ մեթոդը


if __name__ == "__main__":
    main()

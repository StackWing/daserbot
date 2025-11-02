import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# ✅ Այստեղ ուղղակի գրիր բանալիները (առանց getenv)
OPENAI_API_KEY = "OPENAI_API_KEY"
TELEGRAM_TOKEN = "TELEGRAM_TOKEN"

if not OPENAI_API_KEY or not TELEGRAM_TOKEN:
    raise RuntimeError("OPENAI_API_KEY կամ TELEGRAM_TOKEN չեն սահմանված միջավայրում։")

# 🧠 Կապվիր OpenAI-ի հետ
client = OpenAI(api_key=OPENAI_API_KEY)

client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO)

# 🧠 Սկսելու հրահանգ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Բարև 👋 Ես AI ուսումնական բոտն եմ։ Կարող եմ օգնել մաթեմատիկայում, ֆիզիկայում, քիմիայում, լեզուներում և այլ առարկաներում։\n"
        "Ուղարկիր հարցդ, ես կտամ ճիշտ պատասխանը։"
    )

# 📘 Հարցերի վերլուծություն և պատասխան
async def solve_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    prompt = f"""
    Դու խելացի ուսումնական օգնական ես։
    Օգտագործողը կարող է հարցնել տարբեր առարկաներից՝ մաթեմատիկա, հանրահաշիվ, երկրաչափություն, ֆիզիկա, քիմիա, կենսաբանություն, աշխարհագրություն, ռուսերեն, անգլերեն։
    Քո նպատակն է տալ միայն ճիշտ պատասխանը՝ առանց ավել բացատրության (բացատրություն միայն եթե անհրաժեշտ է հասկանալու համար)։
    Հարցը՝ {user_text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Դու ուսումնական օգնական ես, ով պատասխանում է ճշգրիտ և հակիրճ։"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        answer = response.choices[0].message.content.strip()
        await update.message.reply_text(answer)

    except Exception as e:
        print("❌ OPENAI ERROR:", e)
        await update.message.reply_text("⚠️ Սխալ տեղի ունեցավ։ Փորձիր կրկին։")


# 🚀 Գլխավոր ֆունկցիա
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve_question))
    print("🤖 SmartEduBot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

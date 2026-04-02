import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# 👇 PUT YOUR TELEGRAM ID HERE
USERS = {
    1839642283: "2026-05-01",
}

def is_user_allowed(user_id):
    if user_id not in USERS:
        return False
    expiry = datetime.strptime(USERS[user_id], "%Y-%m-%d")
    return datetime.now() < expiry

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    if not is_user_allowed(user_id):
        await update.message.reply_text("❌ Subscription required.")
        return

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=user_text
    )

    reply = response.output_text
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("Bot is running...")
app.run_polling()
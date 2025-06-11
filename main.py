
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram_interface import handle_add_product
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("add_product", handle_add_product))

print("✅ Bot is polling Telegram...")
app.run_polling()

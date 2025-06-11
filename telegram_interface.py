
from telegram import Update
from telegram.ext import ContextTypes

async def handle_add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a product URL.")
        return
    url = context.args[0]
    await update.message.reply_text(f"🔍 Received product URL: {url}\nScraping form fields now...")

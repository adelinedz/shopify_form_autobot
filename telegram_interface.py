
from telegram import Update
from telegram.ext import ContextTypes
from form_parser import parse_form_fields

async def handle_add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a Shopify product URL.")
        return

    url = context.args[0]
    await update.message.reply_text(f"🔍 Received product URL: {url}\nScraping form fields now...")

    try:
        fields = parse_form_fields(url)
    except Exception as e:
        await update.message.reply_text(f"❌ Error scraping page: {str(e)}")
        return

    if isinstance(fields, dict) and "error" in fields:
        await update.message.reply_text(f"⚠️ {fields['error']}")
        return

    response_lines = ["✅ *Form fields detected:*\n"]
    for field in fields:
        label = field.get("label", "(no label)")
        field_type = field.get("type", "?")
        response_lines.append(f"- {label} ({field_type})")
        if field_type == "dropdown":
            options = field.get("options", [])
            preview = ", ".join(options[:3]) + ("..." if len(options) > 3 else "")
            response_lines.append(f"  Options: {preview}")

    await update.message.reply_text("\n".join(response_lines), parse_mode="Markdown")

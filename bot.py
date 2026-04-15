import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import httpx

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

async def quickdive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /quickdive [your thought]")
        return
    
    thought = " ".join(context.args)
    await update.message.reply_text(f"Diving into: {thought}\n\nSearching...")
    
    # Call Claude API here (we'll set this up)
    response = "Quick dive research incoming..."
    await update.message.reply_text(response)

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("quickdive", quickdive))
    
    async with app:
        await app.run_polling()

if __name__ == "__main__":
    main()

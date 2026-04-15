import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from anthropic import Anthropic

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

client = Anthropic(api_key=CLAUDE_API_KEY)

QUICKDIVE_SYSTEM_PROMPT = """You are running the Quick Dive skill for Saffie.

When given a thought, do the following:
1. Run 3 web searches: one for current data, one for the counterargument, one for the practical angle.
2. Synthesize into a 2-3 minute conversational response with four parts:
   - What's actually true (key data point)
   - The pushback (counterargument or nuance)
   - The practical angle (how people deal with it, tied to Saffie's context if relevant)
   - The takeaway (one-sentence frame)
3. End with: "Want to drill into any of those angles? Or move on?"

Tone: conversational, no preamble, no bullet points, full sentences. Saffie is a trader and triathlete based in Amsterdam. Keep responses tight."""

async def quickdive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /quickdive [your thought]")
        return
    
    thought = " ".join(context.args)
    await update.message.reply_text(f"Diving into: {thought}")
    
    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1500,
            system=QUICKDIVE_SYSTEM_PROMPT,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": thought}]
        )
        
        response_parts = []
        for block in message.content:
            if hasattr(block, "text") and block.text:
                response_parts.append(block.text)
        
        response_text = "\n".join(response_parts) if response_parts else "No text response generated. Check API logs."
        
        # Telegram has a 4096 char limit per message
        if len(response_text) > 4000:
            response_text = response_text[:4000] + "..."
        
        await update.message.reply_text(response_text)
    except Exception as e:
        await update.message.reply_text(f"Error: {type(e).__name__}: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("quickdive", quickdive))
    app.run_polling()

if __name__ == "__main__":
    main()

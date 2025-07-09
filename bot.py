from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from keep_alive import keep_alive  # 👈 Flask server for uptime

TOKEN = "7303738732:AAGE0rev64-g-v9AtpFcHbKXbvXPxyMDQqU"
SHRINKME_API = "c3a2e846fc7413b6af5a19fba7c75f089e06f6ae"

def start(update, context):
    update.message.reply_text("👋 Send me a keyword to get a short download link!")

def handle_message(update, context):
    text = update.message.text.strip()
    original_url = f"https://google.com/search?q={text.replace(' ', '+')}"
    shorten_url = f"https://shrinkme.io/api?api={SHRINKME_API}&url={original_url}&alias={text.replace(' ', '')}"

    print(f"🔎 Generating link for: {text}")
    print(f"🔗 Original URL: {original_url}")
    print(f"🌐 API Request: {shorten_url}")

    try:
        response = requests.get(shorten_url).json()
        print("📥 API Response:", response)

        if response['status'] == 'success':
            short = response.get('shortenedUrl') or response.get('shortened')  # fallback
            update.message.reply_text(f"🔗 Link:\n{short}")
        else:
            update.message.reply_text("❌ Error creating short link.")
    except Exception as e:
        print("💥 Error:", e)
        update.message.reply_text("⚠️ Something went wrong while shortening the link.")

def main():
    keep_alive()  # 👈 Start Flask server to keep Replit alive
    print("🚀 Bot is starting...")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

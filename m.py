import telebot
import time
import os
from num import get_number_details

# --- CONFIGURATION ---
TOKEN = '8609540387:AAF_wXfX_lc6yc3OQokpAilUjaRPFDdiwQc'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🔥 **PREMIUM MULTI-TOOL BOT** 🔥\n\n"
        "Ready to fetch details from Database.\n\n"
        "📌 **Command:**\n"
        "👉 `/info <number>` - Get Full Details\n\n"
        "DEVELOPER: @SASTA_DEVELOPER"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['info'])
def handle_info(message):
    text = message.text.split()
    if len(text) > 1:
        number = text[1]
        sent_msg = bot.reply_to(message, "🔍 **Searching Database... Please wait.**", parse_mode="Markdown")
        
        try:
            # num.py function call
            full_report = get_number_details(number)
            bot.edit_message_text(full_report, message.chat.id, sent_msg.message_id, parse_mode="Markdown")
        except Exception as e:
            bot.edit_message_text(f"❌ **System Error:** {str(e)}", message.chat.id, sent_msg.message_id)
    else:
        bot.reply_to(message, "📝 **Usage:** `/info +91XXXXXXXXXX`", parse_mode="Markdown")

if __name__ == "__main__":
    print("🚀 BOT IS STARTING...")
    print("✅ Token Verified!")
    print("📡 Connected to API Market...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Polling Error: {e}")
            time.sleep(5)
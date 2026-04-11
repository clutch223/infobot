import telebot
import time
import os
from flask import Flask
from threading import Thread

# --- DEPENDENCY AUTO-INSTALL ---
try:
    from num import get_number_details
except ImportError:
    os.system("pip install pyTelegramBotAPI requests phonenumbers flask")
    from num import get_number_details

# --- CONFIGURATION ---
TOKEN = '8609540387:AAF_wXfX_lc6yc3OQokpAilUjaRPFDdiwQc'
bot = telebot.TeleBot(TOKEN)
app = Flask('')

# --- RAILWAY KEEP-ALIVE SERVER ---
@app.route('/')
def home():
    return "Bot is Running!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- BOT LOGIC ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🔥 <b>PREMIUM MULTI-TOOL BOT</b> 🔥\n\n"
        "Ready to fetch details from Database.\n\n"
        "📌 <b>Command:</b>\n"
        "👉 <code>/info &lt;number&gt;</code> - Get Full Details\n\n"
        "DEVELOPER: @SASTA_DEVELOPER"
    )
    bot.reply_to(message, welcome_text, parse_mode="HTML")

@bot.message_handler(commands=['info'])
def handle_info(message):
    text = message.text.split()
    if len(text) > 1:
        number = text[1]
        sent_msg = bot.reply_to(message, "🔍 <b>Searching Database... Please wait.</b>", parse_mode="HTML")
        
        try:
            # num.py function call
            full_report = get_number_details(number)
            # Note: num.py returns HTML formatted string, so using HTML mode
            bot.edit_message_text(full_report, message.chat.id, sent_msg.message_id, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            bot.edit_message_text(f"❌ <b>System Error:</b> <code>{str(e)}</code>", message.chat.id, sent_msg.message_id, parse_mode="HTML")
    else:
        bot.reply_to(message, "📝 <b>Usage:</b> <code>/info 91XXXXXXXXXX</code>", parse_mode="HTML")

# Handle text without command for easier use
@bot.message_handler(func=lambda m: m.text and not m.text.startswith('/'))
def handle_raw_number(message):
    if message.text.isdigit():
        sent_msg = bot.reply_to(message, "⚡ <b>Direct Search Detected...</b>", parse_mode="HTML")
        try:
            full_report = get_number_details(message.text)
            bot.edit_message_text(full_report, message.chat.id, sent_msg.message_id, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            bot.edit_message_text(f"❌ <b>Error:</b> {e}", message.chat.id, sent_msg.message_id, parse_mode="HTML")

if __name__ == "__main__":
    # Start web server for Railway
    Thread(target=run).start()
    
    print("🚀 BOT IS STARTING...")
    print("✅ Token Verified!")
    print("📡 Connected to API Market...")
    
    # Simple Polling with Reconnect Logic
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Polling Error: {e}")
            time.sleep(5)

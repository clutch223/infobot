import telebot
from telebot import types
import json
import os
import time
from flask import Flask
from threading import Thread

# Version 1.0.2 - Force Cache Refresh
# --- DEPENDENCY CHECK ---
try:
    import phonenumbers
    from num import get_number_details
except ImportError:
    os.system("pip install phonenumbers pyTelegramBotAPI flask requests")
    import phonenumbers
    from num import get_number_details

# --- CONFIGURATION ---
TOKEN = '8609540387:AAF_wXfX_lc6yc3OQokpAilUjaRPFDdiwQc'
bot = telebot.TeleBot(TOKEN)

# --- RAILWAY WEB SERVER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running smoothly!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- KEYBOARDS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🔍 Info", "👤 My Stats")
    return markup

# --- BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # STRICTLY HTML ONLY - NO MARKDOWN TO PREVENT OFFSET 154 ERROR
    welcome_text = (
        "<b>🚀 SASTADEVELOPER BOT ACTIVE</b>\n\n"
        "Bhai, bot Railway par successfully host ho gaya hai!\n\n"
        "Niche diye gaye menu se check karein 👇"
    )
    try:
        # Puraani galtiyon ko clear karne ke liye humne yahan hard-coded HTML rakha hai
        bot.send_message(message.chat.id, welcome_text, parse_mode="HTML", reply_markup=main_menu())
    except Exception as e:
        # Fallback agar HTML mein bhi issue aaye (unlikely)
        bot.send_message(message.chat.id, "Bot Active! Use /info", reply_markup=main_menu())
        print(f"Error in welcome: {e}")

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    if message.text == "🔍 Info":
        bot.reply_to(message, "📝 <b>Usage:</b> <code>/info 91xxxx</code>", parse_mode="HTML")
    
    elif message.text.startswith('/info'):
        args = message.text.split()
        if len(args) > 1:
            num = args[1]
            sent_msg = bot.reply_to(message, "⚡ <b>Searching Database...</b>", parse_mode="HTML")
            try:
                # get_number_details from num.py returns HTML formatted string
                result = get_number_details(num)
                bot.edit_message_text(result, message.chat.id, sent_msg.message_id, parse_mode="HTML", disable_web_page_preview=True)
            except Exception as e:
                bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, sent_msg.message_id)
        else:
            bot.reply_to(message, "❌ Number missing! Example: <code>/info 919876543210</code>", parse_mode="HTML")

if __name__ == "__main__":
    # Start Web Server
    Thread(target=run).start()
    
    # Fix for Error 409: Conflict & Error 400: Parsing
    print("⚠️ Cleaning sessions and starting fresh...")
    bot.delete_webhook()
    time.sleep(2) # Increased delay for Railway safety
    
    print("🚀 Bot Polling Started...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            if "Conflict" in str(e):
                print("❌ Conflict detected, waiting...")
                time.sleep(10)
            else:
                print(f"TeleBot Error: {e}")
                time.sleep(5)

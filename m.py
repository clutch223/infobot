import telebot
from telebot import types
import json
import os
import time
from flask import Flask
from threading import Thread

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
ADMIN_ID = 8787952549 
CHANNEL_ID = '-1001003605767830' 
CHANNEL_LINK = 'https://t.me/+jMe1PNQv_koxNzI1'

bot = telebot.TeleBot(TOKEN)
app = Flask('')
DATA_FILE = "user_database.json"

# --- DATABASE LOGIC ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

user_db = load_data()

# --- RAILWAY WEB SERVER ---
@app.route('/')
def home():
    return "Advanced Bot Engine Online!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- KEYBOARDS (ADVANCED SYSTEM) ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("🔍 Info")
    btn2 = types.KeyboardButton("👤 My Stats")
    btn3 = types.KeyboardButton("🎁 Refer & Earn")
    btn4 = types.KeyboardButton("💎 Plans")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

# --- CHECK JOIN ---
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# --- BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    uid = str(message.from_user.id)
    
    # New User Initialization
    if uid not in user_db:
        user_db[uid] = {"credits": 2, "refers": 0, "plan": "Free"}
        save_data(user_db)

    welcome_text = (
        f"<b>🚀 WELCOME TO SASTADEVELOPER v2.0</b>\n\n"
        f"<b>User ID:</b> <code>{uid}</code>\n"
        f"<b>Balance:</b> <code>{user_db[uid]['credits']} Credits</code>\n\n"
        f"<i>Premium Intelligence at your fingertips.</i>"
    )
    
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
        markup.add(types.InlineKeyboardButton("✅ Check Join", callback_data="check_join"))
        bot.send_message(message.chat.id, "⚠️ <b>Please join our channel to use the bot!</b>", parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, welcome_text, parse_mode="HTML", reply_markup=main_menu())

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    uid = str(message.from_user.id)
    if uid not in user_db:
        user_db[uid] = {"credits": 2, "refers": 0, "plan": "Free"}
        save_data(user_db)

    if message.text == "🔍 Info":
        bot.reply_to(message, "📝 <b>Usage:</b> <code>/info 91xxxx</code>", parse_mode="HTML")
    
    elif message.text == "👤 My Stats":
        stats = (
            f"👤 <b>USER DASHBOARD</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 <b>Credits:</b> {user_db[uid]['credits']}\n"
            f"👥 <b>Refers:</b> {user_db[uid]['refers']}\n"
            f"👑 <b>Plan:</b> {user_db[uid]['plan']}\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        bot.reply_to(message, stats, parse_mode="HTML")

    elif message.text == "🎁 Refer & Earn":
        ref_link = f"https://t.me/{bot.get_me().username}?start={uid}"
        bot.reply_to(message, f"🎁 <b>Invite friends to earn credits!</b>\n\nYour Link: <code>{ref_link}</code>\n\n<i>1 Refer = 5 Credits</i>", parse_mode="HTML")

    elif message.text.startswith('/info'):
        if user_db[uid]['credits'] < 1:
            return bot.reply_to(message, "❌ <b>Insufficient Credits!</b> Invite friends or buy plan.", parse_mode="HTML")
        
        args = message.text.split()
        if len(args) > 1:
            num = args[1]
            sent_msg = bot.reply_to(message, "⚡ <b>Searching Intelligence...</b>", parse_mode="HTML")
            try:
                result = get_number_details(num)
                bot.edit_message_text(result, message.chat.id, sent_msg.message_id, parse_mode="HTML", disable_web_page_preview=True)
                
                # Deduct Credit
                user_db[uid]['credits'] -= 1
                save_data(user_db)
            except Exception as e:
                bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, sent_msg.message_id)
        else:
            bot.reply_to(message, "❌ Number missing!", parse_mode="HTML")

if __name__ == "__main__":
    Thread(target=run).start()
    print("⚠️ Cleaning sessions...")
    bot.delete_webhook()
    time.sleep(2)
    print("🚀 Advanced Bot Engine Started...")
    
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            if "Conflict" in str(e): time.sleep(10)
            else: time.sleep(5)

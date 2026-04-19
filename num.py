import telebot
from telebot import types
import json, os, time
from flask import Flask
from threading import Thread
import num

# --- CONFIGURATION ---
TOKEN = '8609540387:AAF_wXfX_lc6yc3OQokpAilUjaRPFDdiwQc'
ADMIN_ID = 8787952549 
CHANNEL_ID = '-1001003605767830' 
CHANNEL_LINK = 'https://t.me/+jMe1PNQv_koxNzI1'

bot = telebot.TeleBot(TOKEN)
app = Flask('')
DATA_FILE = "user_database.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
            except: return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

user_db = load_data()

@app.route('/')
def home(): return "Bot is Running"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def is_subscribed(user_id):
    if int(user_id) == ADMIN_ID: return True
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return True 

def ensure_user(uid):
    """KeyError Fix: Ensures user exists in DB before any operation"""
    uid = str(uid)
    global user_db
    if uid not in user_db:
        user_db[uid] = {"credits": 5, "refers": 0, "plan": "Free"}
        save_data(user_db)
    return user_db[uid]

@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.from_user.id)
    ensure_user(uid)
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🔍 Info (Num)", "👤 TG-Scan", "👤 My Stats", "🆔 My ID")
    
    if not is_subscribed(message.from_user.id):
        join_mark = types.InlineKeyboardMarkup()
        join_mark.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
        join_mark.add(types.InlineKeyboardButton("✅ Check Join", callback_data="check"))
        bot.send_message(message.chat.id, "⚠️ <b>Please join our channel to use the bot!</b>", parse_mode="HTML", reply_markup=join_mark)
    else:
        bot.send_message(message.chat.id, "🔥 <b>SASTA OSINT READY</b>\n\nCommands:\n- <code>/info &lt;number&gt;</code>\n- <code>/tg &lt;username/id&gt;</code>", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "check")
def check(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Access Granted!")
        start(call.message)
    else: bot.answer_callback_query(call.id, "❌ Join First!", show_alert=True)

@bot.message_handler(commands=['add'])
def add(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        args = message.text.split()
        target, amt = args[1], int(args[2])
        ensure_user(target)
        user_db[target]['credits'] += amt
        save_data(user_db)
        bot.reply_to(message, f"✅ Added {amt} credits to {target}")
    except: bot.reply_to(message, "Usage: /add <id> <amt>")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    uid = str(message.from_user.id)
    # Critical Fix: Register user on every message to prevent KeyErrors
    u_data = ensure_user(uid)
    
    if not is_subscribed(message.from_user.id): return

    if message.text == "🔍 Info (Num)":
        bot.reply_to(message, "Usage: <code>/info 91xxxxxx</code>", parse_mode="HTML")
    elif message.text == "👤 TG-Scan":
        bot.reply_to(message, "Usage: <code>/tg username</code>", parse_mode="HTML")
    elif message.text == "👤 My Stats":
        bot.reply_to(message, f"💰 <b>CREDITS:</b> {u_data.get('credits', 0)}\n👑 <b>PLAN:</b> {u_data.get('plan', 'Free')}", parse_mode="HTML")
    elif message.text == "🆔 My ID":
        bot.reply_to(message, f"Your ID: <code>{uid}</code>", parse_mode="HTML")
        
    elif message.text.startswith('/info'):
        if u_data['credits'] < 1: return bot.reply_to(message, "❌ <b>Insufficient Credits!</b>", parse_mode="HTML")
        args = message.text.split()
        if len(args) > 1:
            m = bot.reply_to(message, "🔍 <b>Searching KYC...</b>", parse_mode="HTML")
            rep = num.get_kyc_details(args[1])
            bot.edit_message_text(rep, message.chat.id, m.message_id, parse_mode="HTML")
            if "💠" in rep: # Only deduct if successful
                user_db[uid]['credits'] -= 1
                save_data(user_db)
        else: bot.reply_to(message, "Usage: /info 91xxxx")

    elif message.text.startswith('/tg'):
        if u_data['credits'] < 1: return bot.reply_to(message, "❌ <b>Insufficient Credits!</b>", parse_mode="HTML")
        args = message.text.split()
        if len(args) > 1:
            m = bot.reply_to(message, "🔍 <b>Scanning Telegram Database...</b>", parse_mode="HTML")
            rep = num.get_tg_details(args[1])
            bot.edit_message_text(rep, message.chat.id, m.message_id, parse_mode="HTML")
            if "💠" in rep: # Only deduct if successful
                user_db[uid]['credits'] -= 1
                save_data(user_db)
        else: bot.reply_to(message, "Usage: /tg username")

if __name__ == "__main__":
    Thread(target=run).start()
    print("🚀 BOT DEPLOYED ON RAILWAY")
    bot.polling(none_stop=True)

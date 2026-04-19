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
            try: return json.load(f)
            except: return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

user_db = load_data()

@app.route('/')
def home(): return "Bot Online"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def is_subscribed(user_id):
    if int(user_id) == ADMIN_ID: return True
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return True 

def register_user(uid):
    uid = str(uid)
    if uid not in user_db:
        user_db[uid] = {"credits": 5, "refers": 0, "plan": "Free"}
        save_data(user_db)
    return user_db[uid]

@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.from_user.id)
    register_user(uid)
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🔍 Info (Num)", "👤 TG-Scan", "👤 My Stats", "🆔 My ID")
    
    if not is_subscribed(message.from_user.id):
        join_mark = types.InlineKeyboardMarkup()
        join_mark.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
        join_mark.add(types.InlineKeyboardButton("✅ Check Join", callback_data="check"))
        bot.send_message(message.chat.id, "⚠️ <b>Join Channel First!</b>", parse_mode="HTML", reply_markup=join_mark)
    else:
        bot.send_message(message.chat.id, "🔥 <b>SASTA OSINT READY</b>\n\n- /info <number>\n- /tg <username>", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "check")
def check(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Done!")
        start(call.message)
    else: bot.answer_callback_query(call.id, "❌ Join First!", show_alert=True)

@bot.message_handler(commands=['add'])
def add(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        args = message.text.split()
        target, amt = args[1], int(args[2])
        if target not in user_db: user_db[target] = {"credits": 0, "refers": 0, "plan": "Free"}
        user_db[target]['credits'] += amt
        save_data(user_db)
        bot.reply_to(message, "✅ Success")
    except: bot.reply_to(message, "Usage: /add id amt")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    uid = str(message.from_user.id)
    u_data = register_user(uid) # KeyError Fix: Always register before access
    
    if not is_subscribed(message.from_user.id): return

    if message.text == "🔍 Info (Num)":
        bot.reply_to(message, "Usage: <code>/info 91xxxx</code>", parse_mode="HTML")
    elif message.text == "👤 TG-Scan":
        bot.reply_to(message, "Usage: <code>/tg username</code>", parse_mode="HTML")
    elif message.text == "👤 My Stats":
        bot.reply_to(message, f"💰 Credits: {u_data['credits']}")
    elif message.text == "🆔 My ID":
        bot.reply_to(message, f"ID: <code>{uid}</code>", parse_mode="HTML")
        
    elif message.text.startswith('/info'):
        if u_data['credits'] < 1: return bot.reply_to(message, "❌ No Credits")
        args = message.text.split()
        if len(args) > 1:
            m = bot.reply_to(message, "🔍 Scanning KYC...")
            rep = num.get_kyc_details(args[1])
            bot.edit_message_text(rep, message.chat.id, m.message_id, parse_mode="HTML")
            if "SASTA" in rep:
                user_db[uid]['credits'] -= 1
                save_data(user_db)

    elif message.text.startswith('/tg'):
        if u_data['credits'] < 1: return bot.reply_to(message, "❌ No Credits")
        args = message.text.split()
        if len(args) > 1:
            m = bot.reply_to(message, "🔍 Deep Scanning TG...")
            rep = num.get_tg_details(args[1])
            bot.edit_message_text(rep, message.chat.id, m.message_id, parse_mode="HTML")
            if "SASTA" in rep:
                user_db[uid]['credits'] -= 1
                save_data(user_db)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling(none_stop=True)

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
def home(): return "Multi-OSINT System Online!"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🔍 Info (Num)", "👤 TG-Scan", "👤 My Stats", "🆔 My ID", "🎁 Refer & Earn")
    return markup

def is_subscribed(user_id):
    if int(user_id) == ADMIN_ID: return True
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return True 

@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.from_user.id)
    if uid not in user_db:
        user_db[uid] = {"credits": 5, "refers": 0, "plan": "Free"}
        save_data(user_db)
        
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
        markup.add(types.InlineKeyboardButton("✅ Check Join", callback_data="check"))
        bot.send_message(message.chat.id, "⚠️ <b>Please join our channel to use the bot!</b>", parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "🔥 <b>SASTA OSINT ENGINE ONLINE</b> 🔥\n\n- Use <code>/info &lt;number&gt;</code> for KYC Details\n- Use <code>/tg &lt;username/id&gt;</code> for TG-to-Number", parse_mode="HTML", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda c: c.data == "check")
def check(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Access Granted!")
        start(call.message)
    else: bot.answer_callback_query(call.id, "❌ Join First!", show_alert=True)

@bot.message_handler(commands=['add'])
def add(message):
    if message.from_user.id != ADMIN_ID: return
    args = message.text.split()
    if len(args) == 3:
        target = args[1]
        amount = int(args[2])
        if target in user_db:
            user_db[target]['credits'] += amount
            save_data(user_db)
            bot.reply_to(message, f"✅ Added {amount} credits to {target}")
        else: bot.reply_to(message, "❌ User not in DB.")

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    uid = str(message.from_user.id)
    if not is_subscribed(message.from_user.id): return

    if message.text == "🔍 Info (Num)":
        bot.reply_to(message, "Usage: <code>/info 91xxxx</code>", parse_mode="HTML")
    elif message.text == "👤 TG-Scan":
        bot.reply_to(message, "Usage: <code>/tg username</code>", parse_mode="HTML")
    elif message.text == "👤 My Stats":
        bot.reply_to(message, f"👤 <b>STATS</b>\n💰 Credits: {user_db[uid].get('credits', 0)}\n👑 Plan: {user_db[uid].get('plan', 'Free')}", parse_mode="HTML")
    elif message.text == "🆔 My ID":
        bot.reply_to(message, f"Your ID: <code>{uid}</code>", parse_mode="HTML")
    elif message.text == "🎁 Refer & Earn":
        bot.reply_to(message, f"Link: <code>https://t.me/{bot.get_me().username}?start={uid}</code>", parse_mode="HTML")

    # --- KYC SCAN COMMAND ---
    elif message.text.startswith('/info'):
        if user_db[uid]['credits'] < 1: return bot.reply_to(message, "❌ Low Credits!")
        args = message.text.split()
        if len(args) > 1:
            m = bot.reply_to(message, "🔍 <b>Searching KYC...</b>", parse_mode="HTML")
            report = num.get_kyc_details(args[1])
            bot.edit_message_text(report, message.chat.id, m.message_id, parse_mode="HTML")
            if "SASTA" in report:
                user_db[uid]['credits'] -= 1
                save_data(user_db)
        else: bot.reply_to(message, "Usage: /info 91xxxx")

    # --- TG SCAN COMMAND ---
    elif message.text.startswith('/tg'):
        if user_db[uid]['credits'] < 1: return bot.reply_to(message, "❌ Low Credits!")
        args = message.text.split()
        if len(args) > 1:
            m = bot.reply_to(message, "🔍 <b>Deep Scanning TG Profile...</b>", parse_mode="HTML")
            report = num.get_tg_details(args[1])
            bot.edit_message_text(report, message.chat.id, m.message_id, parse_mode="HTML")
            if "SASTA" in report:
                user_db[uid]['credits'] -= 1
                save_data(user_db)
        else: bot.reply_to(message, "Usage: /tg username")

if __name__ == "__main__":
    Thread(target=run).start()
    print("🚀 BOT STARTED")
    bot.polling(none_stop=True)

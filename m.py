import telebot
from telebot import types
import json, os, time
from flask import Flask
from threading import Thread
import num # Importing advanced logic

# --- AUTH CONFIG ---
TOKEN = '8609540387:AAF_wXfX_lc6yc3OQokpAilUjaRPFDdiwQc'
ADMIN = 8787952549
CHANNEL_ID = -1001003605767830
CHANNEL_LINK = "https://t.me/+jMe1PNQv_koxNzI1"

bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=10)
app = Flask('')

# --- DATABASE MANAGEMENT ---
DB_FILE = "users.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

db = load_db()

def get_user(uid):
    uid = str(uid)
    if uid not in db:
        db[uid] = {"credits": 10, "role": "Free User", "joined": time.ctime()}
        save_db(db)
    return db[uid]

# --- WEB SERVER (KEEP ALIVE) ---
@app.route('/')
def status(): return "Bot Status: Active"

def run_server(): app.run(host='0.0.0.0', port=8080)

# --- MIDDLEWARES ---
def check_sub(uid):
    if uid == ADMIN: return True
    try:
        member = bot.get_chat_member(CHANNEL_ID, uid)
        return member.status in ['member', 'administrator', 'creator']
    except: return True

# --- COMMANDS ---
@bot.message_handler(commands=['start'])
def welcome(message):
    uid = message.from_user.id
    u_info = get_user(uid)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔍 Number Info", callback_data="btn_info"),
        types.InlineKeyboardButton("👤 TG Scanner", callback_data="btn_tg"),
        types.InlineKeyboardButton("📊 My Account", callback_data="btn_stats")
    )
    markup.add(types.InlineKeyboardButton("📢 Updates Channel", url=CHANNEL_LINK))
    
    welcome_msg = (
        f"🔥 <b>Welcome to SASTA OSINT v2.0</b>\n\n"
        f"Hi {message.from_user.first_name}, ye bot aapko number ki puri details (KYC/Address) nikal kar dega.\n\n"
        f"💰 <b>Your Credits:</b> <code>{u_info['credits']}</code>\n"
        f"👑 <b>Access:</b> <code>{u_info['role']}</code>"
    )
    bot.send_message(message.chat.id, welcome_msg, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('btn_'))
def handle_callbacks(call):
    if not check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Join channel first!", show_alert=True)
        return

    if call.data == "btn_info":
        bot.edit_message_text("📱 <b>Ab number bhejo!</b>\nFormat: <code>/info 9198xxxxxx</code>", 
                             call.message.chat.id, call.message.message_id, parse_mode="HTML")
    elif call.data == "btn_tg":
        bot.edit_message_text("🛰️ <b>TG Username ya ID bhejo!</b>\nFormat: <code>/tg @username</code>", 
                             call.message.chat.id, call.message.message_id, parse_mode="HTML")
    elif call.data == "btn_stats":
        u = get_user(call.from_user.id)
        bot.answer_callback_query(call.id, f"Credits: {u['credits']} | Plan: {u['role']}", show_alert=True)

@bot.message_handler(commands=['info', 'tg'])
def osint_handler(message):
    uid = str(message.from_user.id)
    u_data = get_user(uid)
    
    if not check_sub(message.from_user.id):
        return bot.reply_to(message, f"❌ <b>Pehle Join Karein:</b> {CHANNEL_LINK}", parse_mode="HTML")

    if u_data['credits'] < 1:
        return bot.reply_to(message, "❌ <b>Bhai credits khatam! Admin @SASTADEVELOPER se contact karo.</b>", parse_mode="HTML")

    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "⚠️ <b>Sahi se likho!</b> Example: <code>/info 91xxxx</code>", parse_mode="HTML")

    query = args[1]
    wait = bot.reply_to(message, "⏳ <b>Processing Request...</b>", parse_mode="HTML")
    
    try:
        if message.text.startswith('/info'):
            result = num.get_kyc_details(query)
        else:
            result = num.get_tg_details(query)
            
        bot.edit_message_text(result, message.chat.id, wait.message_id, parse_mode="HTML")
        
        if "💠" in result or "💎" in result or "🛰️" in result:
            db[uid]['credits'] -= 1
            save_db(db)
    except Exception as e:
        bot.edit_message_text(f"❌ <b>Error Occurred:</b> <code>{str(e)}</code>", message.chat.id, wait.message_id, parse_mode="HTML")

# --- ADMIN PANEL ---
@bot.message_handler(commands=['add'])
def add_credits(message):
    if message.from_user.id != ADMIN: return
    try:
        _, target, amt = message.text.split()
        get_user(target)
        db[target]['credits'] += int(amt)
        save_db(db)
        bot.reply_to(message, f"✅ Done! {target} now has {db[target]['credits']} credits.")
    except: bot.reply_to(message, "Usage: /add <id> <amt>")

if __name__ == "__main__":
    Thread(target=run_server).start()
    print("✅ System Online. Anti-Crash Active.")
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(f"Bot Polling Error: {e}")
            time.sleep(5) # Restart after 5 seconds

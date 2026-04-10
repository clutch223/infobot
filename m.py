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

# --- CHECK JOIN (OPTIMIZED) ---
def is_subscribed(user_id):
    if int(user_id) == ADMIN_ID:
        return True
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Join Check Bypass: {e}")
        return True 

# --- BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    uid = str(message.from_user.id)
    
    # Referral Logic
    args = message.text.split()
    if len(args) > 1 and args[1] != uid:
        referrer_id = args[1]
        if uid not in user_db and referrer_id in user_db:
            user_db[referrer_id]['credits'] = user_db[referrer_id].get('credits', 0) + 5
            user_db[referrer_id]['refers'] = user_db[referrer_id].get('refers', 0) + 1
            try: bot.send_message(referrer_id, "🎁 <b>New Referral!</b> +5 Credits.", parse_mode="HTML")
            except: pass

    if uid not in user_db:
        user_db[uid] = {"credits": 5, "refers": 0, "plan": "Free"}
        save_data(user_db)

    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
        markup.add(types.InlineKeyboardButton("✅ Check Join", callback_data="check_join"))
        bot.send_message(message.chat.id, "⚠️ <b>Please join our channel to use the bot!</b>", parse_mode="HTML", reply_markup=markup)
    else:
        welcome_text = f"<b>🚀 WELCOME TO SASTADEVELOPER</b>\n\n<b>Balance:</b> <code>{user_db[uid].get('credits', 0)}</code>"
        bot.send_message(message.chat.id, welcome_text, parse_mode="HTML", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join_callback(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Access Granted!")
        send_welcome(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ Join First!", show_alert=True)

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    uid = str(message.from_user.id)
    
    if not is_subscribed(message.from_user.id):
        return bot.send_message(message.chat.id, "⚠️ <b>Join Channel First!</b>", parse_mode="HTML")

    if uid not in user_db:
        user_db[uid] = {"credits": 5, "refers": 0, "plan": "Free"}
        save_data(user_db)

    if message.text == "🔍 Info":
        bot.reply_to(message, "📝 <b>Usage:</b> <code>/info 91xxxx</code>", parse_mode="HTML")
    
    elif message.text == "👤 My Stats":
        stats = f"👤 <b>STATS</b>\n💰 Credits: {user_db[uid].get('credits', 0)}\n👑 Plan: {user_db[uid].get('plan', 'Free')}"
        bot.reply_to(message, stats, parse_mode="HTML")

    elif message.text == "🎁 Refer & Earn":
        ref_link = f"https://t.me/{bot.get_me().username}?start={uid}"
        bot.reply_to(message, f"🎁 Link: <code>{ref_link}</code>", parse_mode="HTML")

    elif message.text == "💎 Plans":
        bot.reply_to(message, "💎 <b>Premium:</b> Contact @SASTA_DEVELOPER", parse_mode="HTML")

    elif message.text.startswith('/info'):
        if user_db[uid].get('credits', 0) < 1:
            return bot.reply_to(message, "❌ <b>No Credits!</b>", parse_mode="HTML")
        
        args = message.text.split()
        if len(args) > 1:
            # Clean only non-digits, keep 91 if present
            num = ''.join(filter(str.isdigit, args[1]))
            
            sent_msg = bot.reply_to(message, "⚡ <b>Searching...</b>", parse_mode="HTML")
            try:
                # Pass the number as it is, num.py will handle formatting
                result = get_number_details(num)
                bot.edit_message_text(result, message.chat.id, sent_msg.message_id, parse_mode="HTML", disable_web_page_preview=True)
                
                if "SASTADEVELOPER INTELLIGENCE" in result:
                    user_db[uid]['credits'] -= 1
                    save_data(user_db)
            except Exception as e:
                bot.edit_message_text(f"❌ Error: {e}", message.chat.id, sent_msg.message_id, parse_mode="HTML")
        else:
            bot.reply_to(message, "❌ Send number like: /info 918604219543", parse_mode="HTML")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.delete_webhook()
    time.sleep(1)
    print("🚀 Bot Started...")
    bot.polling(none_stop=True)

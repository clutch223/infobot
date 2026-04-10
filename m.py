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
    # Admin is always allowed
    if int(user_id) == ADMIN_ID:
        return True
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception as e:
        # If check fails due to bot not being admin or API lag, allow user to proceed
        print(f"Join Check Error: {e}")
        return True 

# --- BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    uid = str(message.from_user.id)
    
    # Check for referral in start command
    args = message.text.split()
    if len(args) > 1 and args[1] != uid:
        referrer_id = args[1]
        if uid not in user_db and referrer_id in user_db:
            user_db[referrer_id]['credits'] = user_db[referrer_id].get('credits', 0) + 5
            user_db[referrer_id]['refers'] = user_db[referrer_id].get('refers', 0) + 1
            try:
                bot.send_message(referrer_id, f"🎁 <b>New Referral!</b> You earned 5 credits.", parse_mode="HTML")
            except: pass

    # New User Initialization
    if uid not in user_db:
        user_db[uid] = {"credits": 5, "refers": 0, "plan": "Free"}
        save_data(user_db)

    welcome_text = (
        f"<b>🚀 WELCOME TO SASTADEVELOPER v2.0</b>\n\n"
        f"<b>User ID:</b> <code>{uid}</code>\n"
        f"<b>Balance:</b> <code>{user_db[uid].get('credits', 0)} Credits</code>\n\n"
        f"<i>Premium Intelligence at your fingertips.</i>"
    )
    
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
        markup.add(types.InlineKeyboardButton("✅ Check Join", callback_data="check_join"))
        bot.send_message(message.chat.id, "⚠️ <b>Please join our channel to use the bot!</b>", parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, welcome_text, parse_mode="HTML", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join_callback(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Access Granted!")
        send_welcome(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ Not Joined Yet!", show_alert=True)

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    uid = str(message.from_user.id)
    
    # Force Subscribe Check
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
        markup.add(types.InlineKeyboardButton("✅ Check Join", callback_data="check_join"))
        return bot.send_message(message.chat.id, "⚠️ <b>Bhai, pehle channel join karo!</b>", parse_mode="HTML", reply_markup=markup)

    if uid not in user_db:
        user_db[uid] = {"credits": 5, "refers": 0, "plan": "Free"}
        save_data(user_db)

    if message.text == "🔍 Info":
        bot.reply_to(message, "📝 <b>Usage:</b> <code>/info 91xxxx</code>", parse_mode="HTML")
    
    elif message.text == "👤 My Stats":
        stats = (
            f"👤 <b>USER DASHBOARD</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 <b>Credits:</b> {user_db[uid].get('credits', 0)}\n"
            f"👥 <b>Refers:</b> {user_db[uid].get('refers', 0)}\n"
            f"👑 <b>Plan:</b> {user_db[uid].get('plan', 'Free')}\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        bot.reply_to(message, stats, parse_mode="HTML")

    elif message.text == "🎁 Refer & Earn":
        ref_link = f"https://t.me/{bot.get_me().username}?start={uid}"
        bot.reply_to(message, f"🎁 <b>Invite friends to earn credits!</b>\n\nYour Link: <code>{ref_link}</code>\n\n<i>1 Refer = 5 Credits</i>", parse_mode="HTML")

    elif message.text == "💎 Plans":
        plans = (
            "💎 <b>PREMIUM PLANS</b>\n\n"
            "1. <b>Basic:</b> 50 Credits - ₹49\n"
            "2. <b>Ultra:</b> Unlimited - ₹199 (1 Month)\n\n"
            "Contact @SASTA_DEVELOPER to buy."
        )
        bot.reply_to(message, plans, parse_mode="HTML")

    elif message.text.startswith('/info'):
        current_credits = user_db[uid].get('credits', 0)
        if current_credits < 1:
            return bot.reply_to(message, "❌ <b>Insufficient Credits!</b> Invite friends or buy plan.", parse_mode="HTML")
        
        args = message.text.split()
        if len(args) > 1:
            # Clean number: removes all non-digit characters
            num = ''.join(filter(str.isdigit, args[1]))
            
            # Handling common Indian number mistakes
            if len(num) == 12 and num.startswith('91'):
                num = num[2:]
            elif len(num) > 10 and not num.startswith('91'):
                # Handle cases where user might have pasted a long weird number
                num = num[-10:]
            
            sent_msg = bot.reply_to(message, "⚡ <b>Searching Intelligence...</b>", parse_mode="HTML")
            try:
                result = get_number_details(num)
                # Display output first to ensure user sees something
                bot.edit_message_text(result, message.chat.id, sent_msg.message_id, parse_mode="HTML", disable_web_page_preview=True)
                
                # Credit Deduction logic: Deduct if search was somewhat successful
                if "❌" not in result and "⚠️" not in result:
                    user_db[uid]['credits'] -= 1
                    save_data(user_db)
            except Exception as e:
                bot.edit_message_text(f"❌ <b>Search Failed:</b> <code>{str(e)}</code>", message.chat.id, sent_msg.message_id, parse_mode="HTML")
        else:
            bot.reply_to(message, "❌ Number missing! Usage: <code>/info 919876543210</code>", parse_mode="HTML")

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

import requests
import re

# --- PRE-CONFIGURED APIS ---
# In APIs ko update rakhein agar endpoint change hota hai
KYC_CONFIG = {
    "URL": "https://numbe-info-rootxindia-fixed.satyamrajsingh49.workers.dev/",
    "KEY": "rootxindia14may82NA1"
}

TG_CONFIG = {
    "URL": "https://api-rootxindia.vercel.app/",
    "KEY": "sasta_dev_720"
}

def clean_input(text):
    """Faltu characters hatane ke liye"""
    return re.sub(r'\D', '', text)[-10:] if text.isdigit() else text.strip().replace("@", "")

def get_kyc_details(phone):
    """High-Speed KYC Fetcher"""
    num = clean_input(phone)
    if len(num) < 10: return "❌ <b>Bhai, valid 10-digit number toh daalo!</b>"
    
    try:
        session = requests.Session()
        res = session.get(KYC_CONFIG["URL"], params={'key': KYC_CONFIG["KEY"], 'num': num}, timeout=15)
        
        if res.status_code == 200:
            data = res.json()
            # Multi-layer parsing for stability
            api2 = data.get("api-2", {}).get("result", {}).get("results", [])
            api1 = data.get("api-1", {}).get("results", [])
            results = api2 if api2 else api1
            
            if results:
                info = results[0]
                return (
                    f"<b>💎 PREMIUM KYC REPORT 💎</b>\n"
                    f"<code>━━━━━━━━━━━━━━━━━━━━━━━━</code>\n"
                    f"👤 <b>OWNER:</b> <code>{info.get('name', 'N/A').upper()}</code>\n"
                    f"👨‍💼 <b>FATHER:</b> <code>{info.get('fname', 'N/A').upper()}</code>\n"
                    f"🆔 <b>DOC ID:</b> <code>{info.get('id', 'N/A')}</code>\n"
                    f"📱 <b>ALT NO:</b> <code>{info.get('alt', 'N/A')}</code>\n"
                    f"🌐 <b>CIRCLE:</b> <code>{info.get('circle', 'N/A')}</code>\n"
                    f"📍 <b>ADDRESS:</b>\n<code>{info.get('address', 'N/A').replace('!', ' ')}</code>\n"
                    f"<code>━━━━━━━━━━━━━━━━━━━━━━━━</code>\n"
                    f"⚡ <b>POWERED BY:</b> @SASTADEVELOPER"
                )
            return "⚠️ <b>Database mein record nahi mila.</b>"
        return f"❌ <b>Server Error:</b> {res.status_code}"
    except Exception as e:
        return f"📡 <b>Connection Timeout!</b> (Slow Internet)"

def get_tg_details(query):
    """Advanced Telegram Identity Scanner"""
    target = clean_input(query)
    try:
        res = requests.get(TG_CONFIG["URL"], params={'type': 'tg_num', 'key': TG_CONFIG["KEY"], 'query': target}, timeout=15)
        if res.status_code == 200:
            raw = res.json()
            data = raw.get("data", {})
            
            if raw.get("success") or data.get("success"):
                # Result parsing
                res_node = data.get("result", {}) if isinstance(data.get("result"), dict) else {}
                number = data.get("number") or res_node.get("number")
                
                if number:
                    return (
                        f"<b>🛰️ TELEGRAM DATA LEAK 🛰️</b>\n"
                        f"<code>━━━━━━━━━━━━━━━━━━━━━━━━</code>\n"
                        f"📱 <b>MOBILE:</b> <code>+{res_node.get('country_code', '91')}{number}</code>\n"
                        f"🆔 <b>TG ID:</b> <code>{data.get('tg_id', target)}</code>\n"
                        f"🌍 <b>REGION:</b> <code>{res_node.get('country', 'INDIA')}</code>\n"
                        f"📊 <b>STATUS:</b> <code>VERIFIED ✅</code>\n"
                        f"<code>━━━━━━━━━━━━━━━━━━━━━━━━</code>\n"
                        f"⚡ <b>POWERED BY:</b> @SASTADEVELOPER"
                    )
            return f"❌ <b>Error:</b> {data.get('msg', 'User not found in leak database.')}"
        return "⚠️ <b>API currently offline.</b>"
    except:
        return "📡 <b>Scan failed due to network lag.</b>"

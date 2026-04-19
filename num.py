import requests

# --- CONFIGURATIONS ---
KYC_API_URL = "https://numbe-info-rootxindia-fixed.satyamrajsingh49.workers.dev/"
KYC_API_KEY = "rootxindia14may82NA1"

TG_API_URL = "https://api-rootxindia.vercel.app/"
TG_API_KEY = "sasta_dev_720"

def get_kyc_details(phone_number):
    """Number to Details (KYC/Address)"""
    clean_num = "".join(filter(str.isdigit, phone_number))[-10:]
    params = {'key': KYC_API_KEY, 'num': clean_num}
    
    try:
        res = requests.get(KYC_API_URL, params=params, timeout=25)
        if res.status_code == 200:
            data = res.json()
            # Try API-2 first, then API-1
            results = data.get("api-2", {}).get("result", {}).get("results", [])
            if not results:
                results = data.get("api-1", {}).get("results", [])
            
            if results:
                item = results[0]
                report = f"<b>💠 <u>SASTA KYC SCAN</u> 💠</b>\n"
                report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                report += f"👤 <b>NAME:</b> <b>{item.get('name', 'N/A').upper()}</b>\n"
                report += f"┣ <b>FATHER:</b> {item.get('fname', 'N/A').upper()}\n"
                report += f"🆔 <b>KYC DOCUMENTS</b>\n"
                report += f"┣ <b>DOC ID:</b> <code>{item.get('id', 'N/A')}</code>\n"
                report += f"┣ <b>ALT NO:</b> <code>{item.get('alt', 'N/A')}</code>\n"
                report += f"┗ <b>CIRCLE:</b> <code>{item.get('circle', 'N/A')}</code>\n\n"
                report += f"📍 <b>LOCATION DATA</b>\n"
                report += f"┗ <b>ADDRESS:</b> <code>{item.get('address', 'N/A').replace('!', ' ')}</code>\n"
                report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n👑 <b>BY:</b> @SASTADEVELOPER"
                return report
            return "❌ <b>No records found in KYC Database.</b>"
        return f"⚠️ <b>API Error:</b> {res.status_code}"
    except:
        return "❌ <b>KYC Timeout:</b> Server is slow."

def get_tg_details(query):
    """TG ID/User to Number (Vercel API)"""
    query = str(query).strip().replace("@", "")
    params = {'type': 'tg_num', 'key': TG_API_KEY, 'query': query}
    
    try:
        res = requests.get(TG_API_URL, params=params, timeout=25)
        if res.status_code == 200:
            full = res.json()
            
            # Deep Parsing based on Screenshot 632980
            # Path: data -> data -> result -> number
            d1 = full.get("data", {})
            d2 = d1.get("data", {}) if isinstance(d1.get("data"), dict) else d1
            res_node = d2.get("result", {})
            
            if d2.get("success") or full.get("success"):
                num = d2.get("number") or res_node.get("number") or "N/A"
                tgid = d2.get("tg_id") or res_node.get("tg_id") or query
                c_code = res_node.get("country_code") or "+91"
                
                report = f"<b>💠 <u>SASTA TG-SCAN</u> 💠</b>\n"
                report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                report += f"📱 <b>IDENTIFIED NUMBER:</b>\n"
                report += f"┗ <b><code>{c_code}{num}</code></b>\n\n"
                report += f"👤 <b>TELEGRAM PROFILE</b>\n"
                report += f"┣ <b>TG ID:</b> <code>{tgid}</code>\n"
                report += f"┣ <b>REGION:</b> <code>{res_node.get('country','India')}</code>\n"
                report += f"┗ <b>STATUS:</b> <code>{d2.get('msg','Found')}</code>\n"
                report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n👑 <b>BY:</b> @SASTADEVELOPER"
                return report
            return "❌ <b>Telegram ID/Username not in Database.</b>"
        return "⚠️ <b>TG API Down.</b>"
    except Exception as e:
        return f"❌ <b>Error:</b> API Timeout."

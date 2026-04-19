import requests
import time

# --- CONFIGURATIONS ---
KYC_API_URL = "https://numbe-info-rootxindia-fixed.satyamrajsingh49.workers.dev/"
KYC_API_KEY = "rootxindia14may82NA1"

TG_API_URL = "https://api-rootxindia.vercel.app/"
TG_API_KEY = "sasta_dev_720"

def get_kyc_details(phone_number):
    """System 1: Number to Details (KYC/Address)"""
    clean_num = "".join(filter(str.isdigit, phone_number))[-10:]
    params = {'key': KYC_API_KEY, 'num': clean_num}
    
    # Retry logic to fix "Read timed out"
    for attempt in range(2): 
        try:
            res = requests.get(KYC_API_URL, params=params, timeout=25)
            if res.status_code == 200:
                data = res.json()
                results = data.get("api-2", {}).get("result", {}).get("results", [])
                if not results: results = data.get("api-1", {}).get("results", [])
                
                if results:
                    item = results[0]
                    report = f"<b>💠 <u>SASTA KYC SCAN</u> 💠</b>\n"
                    report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    report += f"👤 <b>NAME:</b> <b>{item.get('name', 'N/A').upper()}</b>\n"
                    report += f"┣ <b>FATHER:</b> {item.get('fname', 'N/A').upper()}\n"
                    report += f"┣ <b>DOC ID:</b> <code>{item.get('id', 'N/A')}</code>\n"
                    report += f"┗ <b>ADDR:</b> <code>{item.get('address', 'N/A').replace('!', ' ')}</code>\n"
                    report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n👑 <b>BY:</b> @SASTADEVELOPER"
                    return report
                return "❌ <b>No records found in KYC Database.</b>"
            time.sleep(1)
        except Exception as e:
            if attempt == 1: return f"❌ <b>KYC Timeout:</b> Server is not responding. Try again later."
    return "❌ <b>KYC System Busy.</b>"

def get_tg_details(query):
    """System 2: TG ID/User to Number (Vercel)"""
    query = query.strip().replace("@", "")
    params = {'type': 'tg_num', 'key': TG_API_KEY, 'query': query}
    
    try:
        res = requests.get(TG_API_URL, params=params, timeout=25)
        if res.status_code == 200:
            data = res.json()
            if data.get("success") or data.get("data", {}).get("success"):
                d = data.get("data", {})
                r = d.get("result", {})
                num = r.get("number") or d.get("number") or "N/A"
                report = f"<b>💠 <u>SASTA TG-TO-NUMBER</u> 💠</b>\n"
                report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                report += f"📱 <b>NUMBER:</b> <code>+{r.get('country_code','91')}{num}</code>\n"
                report += f"┣ <b>TG ID:</b> <code>{d.get('tg_id', 'N/A')}</code>\n"
                report += f"┗ <b>MSG:</b> <code>{d.get('msg','Success')}</code>\n"
                report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n👑 <b>BY:</b> @SASTADEVELOPER"
                return report
            return "❌ <b>Telegram ID/Username not found in DB.</b>"
        return f"⚠️ <b>TG API Error:</b> {res.status_code}"
    except:
        return "❌ <b>TG System Timeout:</b> Vercel server is slow."

import requests

# --- CONFIGURATIONS ---
# API 1: Number to KYC/Address (Old System)
KYC_API_URL = "https://numbe-info-rootxindia-fixed.satyamrajsingh49.workers.dev/"
KYC_API_KEY = "rootxindia14may82NA1"

# API 2: TG Username/ID to Number (New System)
TG_API_URL = "https://api-rootxindia.vercel.app/"
TG_API_KEY = "sasta_dev_720"

def get_number_details(query):
    try:
        query = query.strip().replace("@", "")
        
        # --- AUTO DETECTION LOGIC ---
        # Agar query sirf numbers hai aur length 10-12 hai -> Scan Address/KYC
        if query.isdigit() and (len(query) == 10 or (len(query) == 12 and query.startswith('91'))):
            return scan_kyc_info(query)
        else:
            # Baaki cases (Username/ID) -> Scan Telegram to Number
            return scan_tg_to_num(query)
            
    except Exception as e:
        return f"❌ <b>Error:</b> <code>{str(e)}</code>"

def scan_kyc_info(phone_number):
    """System 1: Number to Details (KYC/Address)"""
    clean_num = phone_number[-10:] 
    params = {'key': KYC_API_KEY, 'num': clean_num}
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        res = requests.get(KYC_API_URL, params=params, headers=headers, timeout=20)
        report = f"<b>💠 <u>SASTA OSINT: KYC SCAN</u> 💠</b>\n"
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        if res.status_code == 200:
            data = res.json()
            # Parsing from your screenshot structure
            results = data.get("api-2", {}).get("result", {}).get("results", [])
            if not results: results = data.get("api-1", {}).get("results", [])
            
            if results:
                item = results[0]
                report += f"👤 <b>NAME:</b> <b>{item.get('name', 'N/A').upper()}</b>\n"
                report += f"┣ <b>FATHER:</b> {item.get('fname', 'N/A').upper()}\n"
                report += f"┣ <b>DOC ID:</b> <code>{item.get('id', 'N/A')}</code>\n"
                report += f"┣ <b>CIRCLE:</b> <code>{item.get('circle', 'N/A')}</code>\n"
                report += f"┗ <b>ADDR:</b> <code>{item.get('address', 'N/A').replace('!', ' ')}</code>\n"
            else:
                report += "❌ <b>No KYC record found.</b>\n"
        else:
            report += f"⚠️ <b>KYC API Error:</b> {res.status_code}\n"
            
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n👑 <b>BY:</b> @SASTADEVELOPER"
        return report
    except: return "❌ KYC API Timeout."

def scan_tg_to_num(tg_query):
    """System 2: TG ID/User to Number (Vercel)"""
    params = {'type': 'tg_num', 'key': TG_API_KEY, 'query': tg_query}
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        res = requests.get(TG_API_URL, params=params, headers=headers, timeout=20)
        report = f"<b>💠 <u>SASTA OSINT: TG SCAN</u> 💠</b>\n"
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        if res.status_code == 200:
            data = res.json()
            if data.get("success") or data.get("data", {}).get("success"):
                d = data.get("data", {})
                r = d.get("result", {})
                num = r.get("number") or d.get("number") or "N/A"
                tgid = d.get("tg_id") or r.get("tg_id") or "N/A"
                
                report += f"📱 <b>NUMBER:</b> <code>+{r.get('country_code','91')}{num}</code>\n"
                report += f"┣ <b>TG ID:</b> <code>{tgid}</code>\n"
                report += f"┣ <b>COUNTRY:</b> <code>{r.get('country','India')}</code>\n"
                report += f"┗ <b>MSG:</b> <code>{d.get('msg','Success')}</code>\n"
            else:
                report += "❌ <b>TG record not found.</b>\n"
        else:
            report += f"⚠️ <b>TG API Error:</b> {res.status_code}\n"
            
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n👑 <b>BY:</b> @SASTADEVELOPER"
        return report
    except: return "❌ TG API Timeout."

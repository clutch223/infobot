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
    
    try:
        res = requests.get(KYC_API_URL, params=params, timeout=25)
        if res.status_code == 200:
            data = res.json()
            # Parsing logic based on image 632144.jpg
            results = data.get("api-2", {}).get("result", {}).get("results", [])
            if not results: results = data.get("api-1", {}).get("results", [])
            
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
        return f"⚠️ <b>Error:</b> Server returned {res.status_code}"
    except:
        return "❌ <b>KYC Timeout:</b> Server is slow. Please try again."

def get_tg_details(query):
    """System 2: TG ID/User to Number (Vercel API)"""
    query = query.strip().replace("@", "")
    # Link format: https://api-rootxindia.vercel.app/?type=tg_num&key=sasta_dev_720&query=QUERY
    params = {
        'type': 'tg_num',
        'key': TG_API_KEY,
        'query': query
    }
    
    try:
        res = requests.get(TG_API_URL, params=params, timeout=25)
        if res.status_code == 200:
            full_resp = res.json()
            # Parsing logic based on image 632980.jpg
            # Response structure: {"data": {"data": {"result": {...}, "success": true, "tg_id": "..."}}}
            
            outer_data = full_resp.get("data", {})
            inner_data = outer_data.get("data", {}) if isinstance(outer_data.get("data"), dict) else outer_data
            result_node = inner_data.get("result", {})
            
            if inner_data.get("success") == True or inner_data.get("success") == "true":
                num = inner_data.get("number") or result_node.get("number") or "N/A"
                tg_id = inner_data.get("tg_id") or result_node.get("tg_id") or "N/A"
                c_code = result_node.get("country_code") or "+91"
                country = result_node.get("country") or "India"
                
                report = f"<b>💠 <u>SASTA TG-TO-NUMBER</u> 💠</b>\n"
                report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                report += f"📱 <b>IDENTIFIED NUMBER:</b>\n"
                report += f"┗ <b><code>{c_code}{num}</code></b>\n\n"
                report += f"👤 <b>TELEGRAM PROFILE</b>\n"
                report += f"┣ <b>TG ID:</b> <code>{tg_id}</code>\n"
                report += f"┣ <b>REGION:</b> <code>{country}</code>\n"
                report += f"┗ <b>STATUS:</b> <code>{inner_data.get('msg', 'Details fetched')}</code>\n"
                
                # Handling Limits if present
                req_left = full_resp.get("req_left") or "N/A"
                report += f"\n📊 <b>LIMITS:</b> <code>{req_left} Queries left</code>\n"
                report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n👑 <b>BY:</b> @SASTADEVELOPER"
                return report
            
            return f"❌ <b>TG SCAN FAILED:</b> {inner_data.get('msg', 'Username/ID not found.')}"
        return f"⚠️ <b>TG API Error:</b> {res.status_code}"
    except Exception as e:
        return f"❌ <b>TG System Error:</b>\n<code>{str(e)}</code>"

import requests

# --- CONFIGURATION ---
API_BASE_URL = "https://numbe-info-rootxindia-fixed.satyamrajsingh49.workers.dev/"
API_KEY = "rootxindia14may82NA1"

def get_number_details(phone_number):
    try:
        # Clean number for API
        clean_number = "".join(filter(str.isdigit, phone_number))
        
        # Handle 12-digit numbers
        if len(clean_number) == 12 and clean_number.startswith('91'):
            clean_number = clean_number[2:]
            
        params = {'key': API_KEY, 'num': clean_number}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(API_BASE_URL, params=params, headers=headers, timeout=20)

        report = f"<b>💠 <u>SASTADEVELOPER INTELLIGENCE</u> 💠</b>\n"
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        report += f"🎯 <b>TARGET:</b> <code>{clean_number}</code>\n"
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        if response.status_code == 200:
            data = response.json()
            results = []
            
            # EXACT PARSING AS PER SCREENSHOT
            # API-2 structure: api-2 -> result -> results -> []
            if "api-2" in data and data["api-2"].get("success"):
                api2_obj = data["api-2"].get("result", {})
                results = api2_obj.get("results", [])
            
            # Fallback to API-1: api-1 -> results -> []
            if not results and "api-1" in data:
                results = data["api-1"].get("results", [])

            if results:
                # Sirf unique records dikhane ke liye
                seen_ids = set()
                found_any = False
                
                for item in results:
                    res_id = item.get('id') or item.get('ID') or 'N/A'
                    
                    if res_id not in seen_ids:
                        seen_ids.add(res_id)
                        found_any = True
                        
                        name = item.get('name') or item.get('NAME') or 'N/A'
                        fname = item.get('fname') or item.get('FNAME') or 'N/A'
                        address = item.get('address') or item.get('ADDRESS') or 'N/A'
                        circle = item.get('circle') or 'N/A'
                        alt = item.get('alt') or 'N/A'
                        
                        # Clean Address formatting
                        clean_address = address.replace('!', ' ').strip()
                        
                        report += f"👤 <b>IDENTITY PROFILE</b>\n"
                        report += f"┣ <b>NAME:</b> <b>{name.upper()}</b>\n"
                        report += f"┗ <b>FATHER:</b> <b>{fname.upper()}</b>\n\n"
                        
                        report += f"🆔 <b>KYC DOCUMENTS</b>\n"
                        report += f"┣ <b>DOC ID:</b> <code>{res_id}</code>\n"
                        report += f"┣ <b>ALT NO:</b> <code>{alt}</code>\n"
                        report += f"┗ <b>CIRCLE:</b> <code>{circle}</code>\n\n"
                        
                        report += f"📍 <b>LOCATION DATA</b>\n"
                        report += f"┗ <b>ADDRESS:</b> <code>{clean_address}</code>\n"
                        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                
                if not found_any:
                    report += "❌ <b>STATUS:</b> No valid records found.\n"
            else:
                report += "❌ <b>STATUS:</b> Data not found in Database.\n"
        else:
            report += f"⚠️ <b>API Error:</b> Code {response.status_code}\n"
            report += f"<i>Check your API Key or connection.</i>\n"

        report += f"👑 <b>POWERED BY:</b> @SASTADEVELOPER\n"
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        return report
    except Exception as e:
        return f"❌ <b>CRITICAL FAILURE:</b>\n<code>{str(e)}</code>"

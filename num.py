import requests
import phonenumbers
from phonenumbers import geocoder, carrier

# --- CONFIGURATION ---
API_BASE_URL = "https://number-info-rootxindia.satyamrajsingh49.workers.dev/"
API_KEY = "rootxpaidh"
CHANNEL_URL = "https://t.me/+jMe1PNQv_koxNzI1"

def get_number_details(phone_number):
    """
    Stable logic that worked in terminal
    """
    try:
        # Cleaning for API: remove +, spaces, and ensure it's just digits
        clean_number = "".join(filter(str.isdigit, phone_number))
        
        # If user sends 12 digits starting with 91, we keep it. 
        # If 10 digits, we pass it as is (API might handle India as default)
        
        params = {'key': API_KEY, 'n': clean_number}
        # Increased timeout and added User-Agent to avoid Code 400 on Cloudflare workers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(API_BASE_URL, params=params, headers=headers, timeout=15)

        report = f"<b>💠 <u>SASTADEVELOPER INTELLIGENCE</u> 💠</b>\n"
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        report += f"🎯 <b>TARGET:</b> <code>{clean_number}</code>\n"
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        if response.status_code == 200:
            data = response.json()
            user_data = data[0] if isinstance(data, list) and len(data) > 0 else data
            
            if user_data and isinstance(user_data, dict) and 'name' in user_data:
                report += f"👤 <b>IDENTITY PROFILE</b>\n"
                report += f"┣ <b>NAME:</b> <b>{user_data.get('name', 'N/A').upper()}</b>\n"
                report += f"┗ <b>FATHER:</b> <b>{user_data.get('fname', 'N/A').upper()}</b>\n\n"
                
                report += f"🆔 <b>KYC DOCUMENTS</b>\n"
                report += f"┣ <b>DOC ID:</b> <code>{user_data.get('id', 'N/A')}</code>\n"
                report += f"┗ <b>E-MAIL:</b> <code>{user_data.get('email', 'N/A')}</code>\n\n"
                
                report += f"📍 <b>LOCATION DATA</b>\n"
                report += f"┗ <b>ADDRESS:</b> <code>{user_data.get('address', 'N/A')}</code>\n"
            else:
                report += "❌ <b>STATUS:</b> No records found for this number.\n"
        else:
            # This is where Code 400 was caught
            report += f"⚠️ <b>API Error:</b> Code {response.status_code}\n"
            report += f"<i>Check if API Key is valid or number format is correct.</i>\n"

        report += f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        report += f"👑 <b>POWERED BY:</b> @SASTADEVELOPER\n"
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        return report
    except Exception as e:
        return f"❌ <b>CRITICAL FAILURE:</b>\n<code>{str(e)}</code>"

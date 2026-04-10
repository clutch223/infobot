import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import time

# --- CONFIGURATION ---
API_KEY = "cmnow6gs40001l804b7quiccv" 
API_URL = "https://prod.api.market/api/v1/magicapi/numinfo"

def get_number_details(phone_number):
    try:
        # Step 1: Formatting
        clean_number = phone_number.replace("+", "").replace(" " , "").replace("-", "")
        intl_number = "+" + clean_number if not clean_number.startswith('+') else clean_number
        parsed_basic = phonenumbers.parse(intl_number)
        
        # Step 2: API Call
        response = requests.post(API_URL, headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }, json={"number": clean_number}, timeout=10)

        report = f"🔥 **PREMIUM INTELLIGENCE REPORT** 🔥\n"
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        report += f"📑 **Target:** `{intl_number}`\n"
        report += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        if response.status_code == 200:
            data_list = response.json()
            
            if isinstance(data_list, list) and len(data_list) > 0:
                user_data = data_list[0]
                
                report += f"👤 **NAME INFO**\n"
                report += f"  ┗ Full Name: `{user_data.get('name', 'N/A')}`\n"
                report += f"  ┗ Father: `{user_data.get('fname', 'N/A')}`\n\n"
                
                report += f"📍 **LOCATION & ADDRESS**\n"
                report += f"  ┗ Address: `{user_data.get('address', 'N/A')}`\n"
                report += f"  ┗ Circle: `{user_data.get('circle', 'N/A')}`\n\n"
                
                report += f"📱 **CONNECTIVITY**\n"
                report += f"  ┗ Alternate: `{user_data.get('alt', 'None')}`\n"
                report += f"  ┗ Carrier: `{carrier.name_for_number(parsed_basic, 'en')}`\n"
                report += f"  ┗ Email: `{user_data.get('email', 'N/A')}`\n"
            else:
                report += "⚠️ **NOTICE:** Record not found in leaks.\n"
        else:
            report += f"⚠️ **API Error:** Code {response.status_code}\n"

        report += f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        report += f"🛠️ **BY:** @SASTA_DEVELOPER"
        
        return report

    except Exception as e:
        return f"❌ **Failure:** `{str(e)}`"
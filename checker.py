import os
import base64
import webbrowser
from requests import get
from re import findall

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

# u can decode it at https://www.base64decode.org/ its just for antiskid :D
dontskid = "ZGVmIGNyZWRpdHMoKTogIyBtYWRlIHRoaXMgc28gc2tpZHMgZG9udCBza2lkIGl0IGxvbAogICAgd2ViYnJvd3Nlci5vcGVuKCdodHRwczovL2dpdGh1Yi5jb20vdW5kZXJhZ2VjaGlsZGVyZW4vcm9ibG94LWNvb2tpZS1jaGVja2VyJykKY3JlZGl0cygp"
antiskid = base64.b64decode(dontskid).decode('utf-8')
exec(antiskid)

def check():
    cookie = input("Cookie: ")
    if not cookie:
        print("Invalid Cookie")
        return
    
    response = get('https://users.roblox.com/v1/users/authenticated', cookies={'.ROBLOSECURITY': cookie})
    
    if '"id":' in response.text:
        user_id = response.json()['id']
        
        robux = get(f'https://economy.roblox.com/v1/users/{user_id}/currency', cookies={'.ROBLOSECURITY': cookie}).json()['robux']
        balance_credit_info = get(f'https://billing.roblox.com/v1/credit', cookies={'.ROBLOSECURITY': cookie})
        balance_credit = balance_credit_info.json()['balance']
        balance_credit_currency = balance_credit_info.json()['currencyCode']
        account_settings = get(f'https://www.roblox.com/my/settings/json', cookies={'.ROBLOSECURITY': cookie})
        account_name = account_settings.json()['Name']
        account_display_name = account_settings.json()['DisplayName']
        account_email_verified = account_settings.json()['IsEmailVerified']
        if bool(account_email_verified):
            account_email_verified = f'{account_email_verified} (`{account_settings.json()["UserEmail"]}`)'
        account_age_in_years = round(float(account_settings.json()['AccountAgeInDays'] / 365), 2)
        account_has_premium = account_settings.json()['IsPremium']
        account_has_pin = account_settings.json()['IsAccountPinEnabled']
        account_2step = account_settings.json()['MyAccountSecurityModel']['IsTwoStepEnabled']
        account_transactions = get(f'https://economy.roblox.com/v2/users/{user_id}/transaction-totals?timeFrame=Year&transactionType=summary', cookies={'.ROBLOSECURITY': cookie}).json()
        account_pending_robux = account_transactions['pendingRobuxTotal']
        account_friends = get('https://friends.roblox.com/v1/my/friends/count', cookies={'.ROBLOSECURITY': cookie}).json()['count']
        account_voice_verified = get('https://voice.roblox.com/v1/settings', cookies={'.ROBLOSECURITY': cookie}).json()['isVerifiedForVoice']
        account_gamepasses = get(f'https://www.roblox.com/users/inventory/list-json?assetTypeId=34&cursor=&itemsPerPage=100&pageNumber=1&userId={user_id}', cookies={'.ROBLOSECURITY': cookie})
        check = findall(r'"PriceInRobux":(.*?),', account_gamepasses.text)
        account_gamepasses = str(sum([int(match) if match != "null" else 0 for match in check])) + ' R$'
        account_badges = ', '.join(list(findall(r'"name":"(.*?)"', get(f'https://accountinformation.roblox.com/v1/users/{user_id}/roblox-badges', cookies={'.ROBLOSECURITY': cookie}).text)))
        cls()
        print(f"""
        Account Name: {account_name} ({account_display_name})
        Mail Verified: {account_email_verified}
        Robux: {robux}
        Pending: {account_pending_robux}
        Balance: {balance_credit} {balance_credit_currency}
        Account Age: {account_age_in_years} years
        Premium: {account_has_premium}
        PIN?: {account_has_pin}
        2-Step Verification: {account_2step}
        Friend Count: {account_friends}
        Voice Chat: {account_voice_verified}
        Gamepasses Worth: {account_gamepasses}
        Badges: {account_badges}
        """)
        
    elif 'Unauthorized' in response.text:
        print("Invalid Cookie")
    else:
        print("Error")
        print(response.text)
    
    input("Done Checking! Press Enter To Exit...")  

check()

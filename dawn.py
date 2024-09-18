import requests
import time
import urllib3
import json
from colorama import init, Fore, Style
from fake_useragent import UserAgent
import os
import asyncio
import telegram

CONFIG_FILE = "config.json"

def read_config(filename=CONFIG_FILE):
    try:
        with open(filename, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"{Fore.RED}[X] Error: Configuration file '{filename}' not found.{Style.BRIGHT}")
        return {}
    except json.JSONDecodeError:
        print(f"{Fore.RED}[X] Error: Invalid JSON format in '{filename}'.{Style.BRIGHT}")
        return {}

config = read_config(CONFIG_FILE)
bot_token = config.get("telegram_bot_token")
chat_id = config.get("telegram_chat_id")

if not bot_token or not chat_id:
    print(f"{Fore.RED}[X] Error: Missing 'bot_token' or 'chat_id' in 'config.json'.{Style.BRIGHT}")
    exit(1) 

bot = telegram.Bot(token=bot_token)
keepalive_url = "https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive"
get_points_url = "https://www.aeropres.in/api/atom/v1/userreferral/getpoint"
extension_id = "fpdkjdnhkakefebpekbdhillbhonfjjp"
_v = "1.0.7"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ua = UserAgent()

init(autoreset=True)

def banner():
    os.system("title DAWN Validator" if os.name == "nt" else "clear")
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + Style.BRIGHT + r"""
   ___   ___  _      __ _  __                           
  / _ \ / _ || | /| / // |/ /                           
 / // // __ || |/ |/ //    /                            
/____//_/ |_||__/|__//_/|_/  https://github.com/gilanx04
  _   __ ___    __    ____ ___   ___  ______ ____   ___ 
 | | / // _ |  / /   /  _// _ \ / _ |/_  __// __ \ / _ \
 | |/ // __ | / /__ _/ / / // // __ | / /  / /_/ // , _/
 |___//_/ |_|/____//___//____//_/ |_|/_/   \____//_/|_| 
                                                                                   
    """ + Style.BRIGHT)

def read_account(filename="config.json"):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            accounts = data.get("accounts", [])
            return accounts 
    except FileNotFoundError:
        print(f"{Fore.RED}[X] Error: config file '{filename}' not found.{Style.BRIGHT}")
        return []
    except json.JSONDecodeError:
        print(f"{Fore.RED}[X] Error: Invalid JSON format in '{filename}'.{Style.BRIGHT}")
        return []

def total_points(headers):
    try:
        response = requests.get(get_points_url, headers=headers, verify=False)
        response.raise_for_status()

        json_response = response.json()
        if json_response.get("status"):
            reward_point_data = json_response["data"]["rewardPoint"]
            referral_point_data = json_response["data"]["referralPoint"]
            total_points = (
                reward_point_data.get("points", 0) +
                reward_point_data.get("registerpoints", 0) +
                reward_point_data.get("signinpoints", 0) +
                reward_point_data.get("twitter_x_id_points", 0) +
                reward_point_data.get("discordid_points", 0) +
                reward_point_data.get("telegramid_points", 0) +
                reward_point_data.get("bonus_points", 0) +
                referral_point_data.get("commission", 0)
            )
            return total_points
        else:
            print(f"{Fore.YELLOW}[!] Warning: {json_response.get('message', 'Unknown error when fetching points')}{Style.BRIGHT}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[X] Error: {e}{Style.BRIGHT}")
    return 0

def keep_alive(headers, email):
    keepalive_payload = {
        "username": email,
        "extensionid": extension_id,
        "numberoftabs": 0,
        "_v": _v
    }

    headers["User-Agent"] = ua.random

    try:
        response = requests.post(keepalive_url, headers=headers, json=keepalive_payload, verify=False)
        response.raise_for_status()

        json_response = response.json()
        if 'message' in json_response:
            return True, json_response['message']
        else:
            return False, "Message not found in response"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"{Fore.LIGHTBLUE_EX}[~] Restarting in: {i} seconds", end='\r')
        time.sleep(1)

async def telegram_message(message):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"{Fore.RED}[X] Error sending Telegram message: {e}{Style.BRIGHT}")

async def main():
    banner()
    while True:
        accounts = read_account()
        if not accounts:
            break

        total_points_all_users = 0
        messages = []

        messages.append("📢 DAWN Internet Validator Extension\n")

        for account_index, account in enumerate(accounts):
            email = account["email"]
            token = account["token"]
            headers = { 
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": ua.random
            }

            print(f"{Fore.CYAN}━━━━━━━━━━━━━[ DAWN Validator | Account {account_index + 1} ]━━━━━━━━━━━━━{Style.BRIGHT}")
            print(f"{Fore.MAGENTA}[@] Email: {email}{Style.BRIGHT}")

            points = total_points(headers)
            total_points_all_users += points 
            success, status_message = keep_alive(headers, email)

            if success:
                messages.append(f"""👤 acc: {email}
💰 point: +{points:,.0f} - Alive ✅
""")
                print(f"{Fore.GREEN}[✓] Status: Keep alive recorded{Style.BRIGHT}")
                print(f"{Fore.GREEN}[✓] Request for {email} successful.{Style.BRIGHT}\n")
            else:
                messages.append(f"""👤 acc: {email} - Failed ❌
⚠️ err: {status_message}
""")
                print(f"{Fore.RED}[X] Status: Keep alive failed!{Style.BRIGHT}")
                print(f"{Fore.RED}[X] Error: {status_message}{Style.BRIGHT}\n")

        combined_message = "\n".join(messages)
        combined_message += f"\nAll accounts processed.\nTotal points from all users: 💰 {total_points_all_users:,.0f}\n"

        if combined_message:
            await telegram_message(combined_message)

        countdown(181)
        print(f"\n{Fore.GREEN}[✓] Restarting the process...{Style.BRIGHT}\n")

if __name__ == "__main__":
    asyncio.run(main())

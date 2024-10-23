import requests
import time
import json
import os
import asyncio
import telegram
from colorama import init, Fore, Style
from fake_useragent import UserAgent
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CONFIG_FILE = "config.json"

def read_config(filename=CONFIG_FILE):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"{Fore.RED}[X] Error: {e}{Style.BRIGHT}")
        exit(1)

config = read_config()
bot_token = config.get("telegram_bot_token")
chat_id = config.get("telegram_chat_id")
appid = config.get("appid")

if not all([bot_token, chat_id, appid]):
    print(f"{Fore.RED}[X] Error: Missing 'bot_token', 'chat_id', or 'appid' in 'config.json'.{Style.BRIGHT}")
    exit(1)

bot = telegram.Bot(token=bot_token)
keepalive_url = "https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive"
get_points_url = "https://www.aeropres.in/api/atom/v1/userreferral/getpoint"
extension_id = "fpdkjdnhkakefebpekbdhillbhonfjjp"
_v = "1.0.9"

init(autoreset=True)
ua = UserAgent()

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + Style.BRIGHT + r"""
 ____    ___        ___   _          
|  _ \  / \ \      / / \ | |         
| | | |/ _ \ \ /\ / /|  \| |         
| |_| / ___ \ V  V / | |\  |         
|____/_/ _ \_\_/\_/  |_| \_|     _   
(_)_ __ | |_ ___ _ __ _ __   ___| |_ 
| | '_ \| __/ _ \ '__| '_ \ / _ \ __|
| | | | | ||  __/ |  | | | |  __/ |_ 
|_|_| |_|\__\___|_|  |_| |_|\___|\__|

author: gilanx04
update: officialputuid
    """ + Style.BRIGHT)

def read_accounts():
    return config.get("accounts", [])

def total_points(headers):
    try:
        response = requests.get(f"{get_points_url}?appid={appid}", headers=headers, verify=False)
        response.raise_for_status()
        json_response = response.json()
        
        if json_response.get("success") is False:
            print(f"{Fore.YELLOW}[!] Warning: {json_response.get('message', 'Error fetching points')}{Style.BRIGHT}")
            return 0

        reward_data = json_response["data"]["rewardPoint"]
        referral_data = json_response["data"]["referralPoint"]

        return sum([
            reward_data.get("points", 0),
            reward_data.get("registerpoints", 0),
            reward_data.get("signinpoints", 0),
            reward_data.get("twitter_x_id_points", 0),
            reward_data.get("discordid_points", 0),
            reward_data.get("telegramid_points", 0),
            reward_data.get("bonus_points", 0),
            referral_data.get("commission", 0)
        ])
    except requests.exceptions.RequestException:
        print(f"{Fore.RED}[X] Error fetching points{Style.BRIGHT}")
        return 0

def keep_alive(headers, email):
    payload = {
        "username": email,
        "extensionid": extension_id,
        "numberoftabs": 0,
        "_v": _v
    }
    headers["User-Agent"] = ua.random
    try:
        response = requests.post(f"{keepalive_url}?appid={appid}", headers=headers, json=payload, verify=False)
        response.raise_for_status()
        json_response = response.json()
        return json_response.get("success", False), json_response.get("message", "Keep alive successful.")
    except requests.exceptions.RequestException:
        return False, "Error during keep alive."

async def telegram_message(message):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"{Fore.RED}[X] Error sending Telegram message: {e}{Style.BRIGHT}")

def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"{Fore.LIGHTBLUE_EX}[~] Restarting in: {i} seconds", end='\r')
        time.sleep(1)

async def main():
    banner()
    while True:
        accounts = read_accounts()
        if not accounts:
            break

        total_points_all_users = 0
        messages = ["📢 DAWN Internet Validator Extension\n"]

        for idx, account in enumerate(accounts):
            email = account["email"]
            token = account["token"]
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": ua.random
            }

            print(f"{Fore.CYAN}━━━━━━━━━━━━━[ DAWN Validator | Account {idx + 1} ]━━━━━━━━━━━━━{Style.BRIGHT}")
            print(f"{Fore.MAGENTA}[@] Email: {email}{Style.BRIGHT}")

            points = total_points(headers)
            total_points_all_users += points

            success, status_msg = keep_alive(headers, email)

            # Formatting message for each account
            if success:
                messages.append(f"👤 acc: {email}\n✍️ Info: success, Point: {points:,.0f} and Keep alive recorded!")
                print(f"{Fore.GREEN}[✓] Status: Keep alive recorded!{Style.BRIGHT}")
            else:
                messages.append(f"👤 acc: {email}\n✍️ Info: error, Point: {points:,.0f} and Keep alive failed!")
                print(f"{Fore.RED}[X] Status: {status_msg}{Style.BRIGHT}")

            print(f"{Fore.GREEN if success else Fore.RED}[{ '✓' if success else 'X'}] Total Points: {points:,.0f}{Style.BRIGHT}\n")

        # Sending message to Telegram with total points from all users
        await telegram_message("\n".join(messages) + f"\n\nTotal points from all users: 💰 {total_points_all_users:,.0f}\n")
        countdown(181)
        print(f"{Fore.GREEN}[✓] Restarting the process...{Style.BRIGHT}\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Program closed.{Style.BRIGHT}")

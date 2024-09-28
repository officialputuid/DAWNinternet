# DAWN Internet
Validation of DAWN Internet Validator Extension accounts, Keep Alive Connection, check all points, and send notifications to Telegram.

## Installation
**Clone Repository**
   ```bash
   git clone https://github.com/officialputuid/DAWNinternet && cd DAWNinternet && pip install -r requirements.txt
   ```

**Configuration**
   Edit the `config.json` file in the following format:
   ```json
    {
      "telegram_bot_token": "YOUR_TOKEN_ID FROM @BotFather",
      "telegram_chat_id": "YOUR_CHAT_ID FROM @getmyid_bot",
      "appid": "YOUR_APPID FROM (Inspect - Network - getpoint)",
      "accounts": [
        {
          "email": "example@domain.com",
          "token": "get token? (Inspect - Network - getpoint - Authorization)"
        },
        {
          "email": "example2@domain.com",
          "token": "get token? (Inspect - Network - getpoint - Authorization)"
        }
      ]
    }
   ```
   - `telegram_bot_token`: The Telegram bot token obtained from @BotFather.
   - `telegram_chat_id`: The Telegram chat ID obtained from @getmyid_bot.
   - `appid`: YOUR_APPID FROM (Inspect - Network - getpoint).
   - `accounts`: A list of accounts to be processed. Each account requires an `email` and a `token` obtained from network inspection.

4. **Run the Script**
```bash
python dawn.py
```

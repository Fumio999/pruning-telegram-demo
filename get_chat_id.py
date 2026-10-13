"""Run this once after you've sent a message to your new bot from your own Telegram account.

It prints the chat_id(s) the bot has seen so you can copy the right one
into TELEGRAM_CHAT_ID in .env.
"""

import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    sys.exit("TELEGRAM_BOT_TOKEN is not set in .env")

resp = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", timeout=15)
resp.raise_for_status()
data = resp.json()

if not data.get("result"):
    print("No messages seen yet. Send any message to your bot from your own account, then re-run this script.")
    sys.exit(0)

seen = set()
for update in data["result"]:
    msg = update.get("message") or update.get("channel_post")
    if not msg:
        continue
    chat = msg["chat"]
    key = chat["id"]
    if key in seen:
        continue
    seen.add(key)
    username = chat.get("username", "(no username)")
    name = chat.get("first_name", "")
    print(f"chat_id={chat['id']}  username=@{username}  name={name}")

print("\nCopy the chat_id that matches your account into TELEGRAM_CHAT_ID in .env")

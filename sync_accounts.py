"""Syncs accounts.json with any new chats the bot has seen.

- Chats with a usable Telegram username/name are added automatically.
- Chats without one (e.g. emoji-only display name, no username) prompt for a name.

This polls Telegram once, at the moment you run it — there's no background
listener in this demo, so run this after a new worker has messaged the bot
(e.g. via bot_invite_qr.png).
"""

import json
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

import requests
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent
ACCOUNTS_PATH = ROOT / "accounts.json"

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    sys.exit("TELEGRAM_BOT_TOKEN is not set in .env")

accounts = []
if ACCOUNTS_PATH.exists():
    with open(ACCOUNTS_PATH, encoding="utf-8") as f:
        accounts = json.load(f)

known_ids = {str(a["chat_id"]) for a in accounts}

resp = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", timeout=15)
resp.raise_for_status()
updates = resp.json().get("result", [])

seen = {}
for update in updates:
    msg = update.get("message") or update.get("channel_post")
    if not msg:
        continue
    chat = msg["chat"]
    seen[str(chat["id"])] = chat

new_chats = {cid: chat for cid, chat in seen.items() if cid not in known_ids}

if not new_chats:
    print("新しいアカウントは見つかりませんでした。")
    sys.exit(0)

added = []
for cid, chat in new_chats.items():
    username = chat.get("username") or ""
    candidate = username or chat.get("first_name") or ""
    if any(c.isalnum() for c in candidate):
        name = candidate
    else:
        print(f"chat_id={cid} は表示名/ユーザー名が分かりにくいため（例: 絵文字のみ）、名前を入力してください。")
        name = input("名前: ").strip() or f"Unknown ({cid})"
    accounts.append({"name": name, "username": username, "chat_id": cid})
    added.append((cid, name))

with open(ACCOUNTS_PATH, "w", encoding="utf-8") as f:
    json.dump(accounts, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"{len(added)}件のアカウントを追加しました:")
for cid, name in added:
    print(f"  - {name} (chat_id={cid})")

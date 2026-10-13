"""Interactive picker: choose one or more recipient accounts (or "all"),
then choose one or more work-standard images from output/, and send them
via the Telegram bot to each selected recipient.

- 1 image selected -> sent as a single photo
- 2+ images selected -> sent as one album (media group)
"""

import json
import os
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

from dotenv import load_dotenv

from telegram_api import send_album, send_photo

load_dotenv()

ROOT = Path(__file__).parent
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    sys.exit("TELEGRAM_BOT_TOKEN is not set in .env")

ACCOUNTS_PATH = ROOT / "accounts.json"
OUT_DIR = ROOT / "output"


def account_label(a) -> str:
    return f"{a['name']} (@{a['username']})" if a.get("username") else a["name"]


def load_accounts():
    if not ACCOUNTS_PATH.exists():
        sys.exit(f"{ACCOUNTS_PATH} not found")
    with open(ACCOUNTS_PATH, encoding="utf-8") as f:
        accounts = json.load(f)
    if not accounts:
        sys.exit("accounts.json is empty")
    return accounts


def label_for(path: Path) -> str:
    stem = path.stem
    m = re.match(r"^standard_(\d+)_(.+)$", stem)
    if m:
        num, slug = m.groups()
        return f"作業基準{num}: {slug.replace('_', ' ')}"
    return stem.replace("_", " ")


def load_standards():
    files = sorted(OUT_DIR.glob("*.png"))
    if not files:
        sys.exit(f"No .png files found in {OUT_DIR} — run generate_images.py first")
    return files


def pick_many(items, render):
    for i, item in enumerate(items, 1):
        print(f"  {i}. {render(item)}")
    print("  例: 1 / 1,2 / all")
    while True:
        raw = input("番号を選択してください（カンマ区切りで複数可）: ").strip().lower()
        if raw == "all":
            return items
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        if parts and all(p.isdigit() and 1 <= int(p) <= len(items) for p in parts):
            seen = []
            for p in parts:
                item = items[int(p) - 1]
                if item not in seen:
                    seen.append(item)
            return seen
        print("無効な選択です。もう一度入力してください。")


def main():
    accounts = load_accounts()
    print("送信先アカウントを選択（複数選択可、全員に送る場合は all）:")
    selected_accounts = pick_many(accounts, account_label)

    standards = load_standards()
    print("\n送信する作業基準を選択:")
    selected_standards = pick_many(standards, label_for)

    print(f"\n確認: 以下の{len(selected_accounts)}アカウントに送信します。")
    for a in selected_accounts:
        print(f"  - {account_label(a)}")
    print("送信内容:")
    for s in selected_standards:
        print(f"  - {label_for(s)}")
    if input("送信してよろしいですか？ (y/N): ").strip().lower() != "y":
        print("送信をキャンセルしました。")
        return

    results = []
    for a in selected_accounts:
        chat_id = a["chat_id"]
        try:
            if len(selected_standards) == 1:
                send_photo(TOKEN, chat_id, selected_standards[0])
            else:
                send_album(TOKEN, chat_id, selected_standards)
            results.append((a, True, None))
        except Exception as e:
            results.append((a, False, str(e)))

    print("\n送信結果:")
    for a, ok, err in results:
        status = "成功" if ok else f"失敗 ({err})"
        print(f"  - {account_label(a)}: {status}")


if __name__ == "__main__":
    main()

"""Sends the two pruning work-standard images to TELEGRAM_CHAT_ID as a single
Telegram album (media group), in photo mode.

Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env.
Run generate_images.py first if output/*.png don't exist yet.

For an interactive picker (choose recipient + which standard(s) to send),
use cli_send.py instead.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from telegram_api import send_album

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN:
    sys.exit("TELEGRAM_BOT_TOKEN is not set in .env")
if not CHAT_ID:
    sys.exit("TELEGRAM_CHAT_ID is not set in .env (run get_chat_id.py first)")

OUT_DIR = Path(__file__).parent / "output"
IMAGES = [
    OUT_DIR / "standard_1_cutting_technique.png",
    OUT_DIR / "standard_2_timing_disposal.png",
]

for p in IMAGES:
    if not p.exists():
        sys.exit(f"Missing {p} — run generate_images.py first")

send_album(TOKEN, CHAT_ID, IMAGES)
print(f"Sent {len(IMAGES)} images to chat_id={CHAT_ID}")

"""Generates a QR code linking to the bot's Telegram chat, for onboarding
new workers on-site. Scanning it opens a chat with the bot so they can
send it a first message (required before the bot can message them back).
"""

import os
import sys

import qrcode
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    sys.exit("TELEGRAM_BOT_TOKEN is not set in .env")

resp = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe", timeout=15)
resp.raise_for_status()
me = resp.json()["result"]
username = me["username"]
link = f"https://t.me/{username}"

qr = qrcode.QRCode(border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(link)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

pad = 60
label = f"@{username} をTelegramで開く"
font = ImageFont.truetype(r"C:\Windows\Fonts\meiryo.ttc", 28)

measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
bbox = measure.textbbox((0, 0), label, font=font)
tw = bbox[2] - bbox[0]

canvas_w = max(qr_img.width + pad * 2, tw + pad * 2)
canvas = Image.new("RGB", (canvas_w, qr_img.height + pad * 2 + 50), "white")
canvas.paste(qr_img, ((canvas_w - qr_img.width) // 2, pad))
d = ImageDraw.Draw(canvas)
d.text(((canvas_w - tw) / 2 - bbox[0], qr_img.height + pad + 5), label, font=font, fill="black")

out_path = os.path.join(os.path.dirname(__file__), "bot_invite_qr.png")
canvas.save(out_path)
print(f"Saved {out_path}")
print(f"Link: {link}")

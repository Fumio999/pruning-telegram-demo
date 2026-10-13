"""Thin wrapper around the Telegram Bot API calls used by this project."""

import json

import requests


def send_photo(token: str, chat_id: str, path):
    with open(path, "rb") as f:
        resp = requests.post(
            f"https://api.telegram.org/bot{token}/sendPhoto",
            data={"chat_id": chat_id},
            files={"photo": f},
            timeout=30,
        )
    resp.raise_for_status()
    result = resp.json()
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error: {result}")
    return result


def send_album(token: str, chat_id: str, paths):
    media = [{"type": "photo", "media": f"attach://{p.name}"} for p in paths]
    files = {p.name: open(p, "rb") for p in paths}
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{token}/sendMediaGroup",
            data={"chat_id": chat_id, "media": json.dumps(media)},
            files=files,
            timeout=30,
        )
    finally:
        for f in files.values():
            f.close()
    resp.raise_for_status()
    result = resp.json()
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error: {result}")
    return result

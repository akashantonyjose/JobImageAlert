import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_photo(image_path, caption):
    """Send an image with a caption to your Telegram chat."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing - skipping send.")
        return None

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as f:
        files = {"photo": f}
        # Telegram captions are capped at 1024 characters
        data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption[:1024]}
        resp = requests.post(url, data=data, files=files, timeout=30)

    if resp.status_code != 200:
        print("Telegram send failed:", resp.text)
    return resp

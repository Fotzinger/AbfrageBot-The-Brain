import os

DATA_DIR = os.environ.get("DATA_DIR", "data")
TELEGRAM_BOT_TOKEN = (os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip()
RAPIDAPI_KEY = (os.environ.get("RAPIDAPI_KEY") or "").strip()

print("CONFIG CHECK:")
print("DATA_DIR:", DATA_DIR)
print("TELEGRAM_BOT_TOKEN gesetzt:", bool(TELEGRAM_BOT_TOKEN))
print("RAPIDAPI_KEY gesetzt:", bool(RAPIDAPI_KEY))

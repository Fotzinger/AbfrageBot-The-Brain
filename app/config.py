import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")

print("CONFIG CHECK:")
print("TELEGRAM_BOT_TOKEN gesetzt:", bool(TELEGRAM_BOT_TOKEN))
print("RAPIDAPI_KEY gesetzt:", bool(RAPIDAPI_KEY))

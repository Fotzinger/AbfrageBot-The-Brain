import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '').strip()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '').strip()
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST', '').strip()
SCRAPTIK_USER_ENDPOINT = os.getenv('SCRAPTIK_USER_ENDPOINT', '').strip()
DATA_DIR = os.getenv('DATA_DIR', './data').strip()

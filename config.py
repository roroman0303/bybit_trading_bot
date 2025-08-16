import os
from dotenv import load_dotenv

load_dotenv()

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
MODE = os.getenv("MODE", "paper")  # "paper" или "real"

if not BYBIT_API_KEY or not BYBIT_API_SECRET:
    raise ValueError("API-ключи не установлены. Используйте .env с BYBIT_API_KEY и BYBIT_API_SECRET")
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
    ADMIN_TELEGRAM_ID = os.getenv("ADMIN_TELEGRAM_ID")

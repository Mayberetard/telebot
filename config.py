from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "cookie_store"
APPROVED_ADMINS = [1]  # Replace with your Telegram user ID

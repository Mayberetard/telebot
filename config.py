from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "cookie_store"
OWNER_CONTACT_URL = "https://t.me/YourUsername"

START_IMAGES = [ ]

APPROVED_ADMINS = [1]  # Replace with your Telegram user ID

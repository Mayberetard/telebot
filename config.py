from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "cookie_store"
OWNER_CONTACT_URL = "https://t.me/i100GIFT"

START_IMAGES = ["https://envs.sh/Rgt.jpg" , "https://envs.sh/7tv.jpg" , "https://graph.org/file/dea04b2d615406aeb0181.jpg" , "https://graph.org/file/98b63d3bb84984a68cc76.jpg"]

APPROVED_ADMINS = [5169654373]  # Replace with your Telegram user ID

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from cookies import add_cookie, get_cookie, delete_cookie, is_user_approved, approve_user, list_approved_users
from config import BOT_TOKEN, APPROVED_ADMINS
from worker import run_periodic_requests
import asyncio

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

C_VALUES = ["A1", "B2", "C3", "D4", "E5", "F6"]

async def check_access(message: Message):
    user_id = message.from_user.id
    if user_id in APPROVED_ADMINS or is_user_approved(user_id):
        return True
    await message.answer("❌ You are not authorized to use this bot.")
    return False

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Welcome! Use /add_cookie, /delete_cookie, or /run if approved.")

@dp.message(Command("add_cookie"))
async def cmd_add_cookie(message: Message):
    if not await check_access(message):
        return
    cookie = message.text.replace("/add_cookie", "").strip()
    if not cookie:
        await message.answer("Please provide a cookie after the command.")
        return
    add_cookie(message.from_user.id, cookie)
    await message.answer("✅ Cookie added.")

@dp.message(Command("delete_cookie"))
async def cmd_delete_cookie(message: Message):
    if not await check_access(message):
        return
    delete_cookie(message.from_user.id)
    await message.answer("🗑️ Cookie deleted.")

@dp.message(Command("run"))
async def cmd_run(message: Message):
    if not await check_access(message):
        return
    cookie = get_cookie(message.from_user.id)
    if not cookie:
        await message.answer("❗ No cookie found. Use /add_cookie first.")
        return
    await message.answer("🔁 Starting periodic requests every 15 minutes...")
    asyncio.create_task(run_periodic_requests(message.from_user.id, cookie, message, C_VALUES))

@dp.message(Command("approve"))
async def cmd_approve(message: Message):
    if message.from_user.id not in APPROVED_ADMINS:
        await message.answer("🚫 Only admins can approve users.")
        return
    try:
        uid = int(message.text.replace("/approve", "").strip())
        approve_user(uid)
        await message.answer(f"✅ User {uid} approved.")
    except ValueError:
        await message.answer("⚠️ Usage: /approve <telegram_user_id>")

@dp.message(Command("list_approved"))
async def cmd_list_approved(message: Message):
    if message.from_user.id not in APPROVED_ADMINS:
        return
    users = list_approved_users()
    await message.answer("✅ Approved users:\n" + "\n".join(map(str, users)))

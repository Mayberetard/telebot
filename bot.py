import asyncio
import random

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from cookies import (
    add_cookie, get_cookie, delete_cookie,
    is_user_approved, approve_user, list_approved_users
)
from config import BOT_TOKEN, APPROVED_ADMINS, OWNER_CONTACT_URL, START_IMAGES
from worker import run_periodic_requests

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_tasks = {}
C_VALUES = ["A1", "B2", "C3", "D4", "E5", "F6"]

async def check_access(message: Message):
    uid = message.from_user.id
    if uid in APPROVED_ADMINS or is_user_approved(uid):
        return True
    await message.answer("❌ You are not authorized to use this bot.")
    return False

@dp.message(Command("start"))
async def cmd_start(message: Message):
    photo_url = random.choice(START_IMAGES)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Contact Owner", url=OWNER_CONTACT_URL)]
    ])
    await message.answer_photo(photo_url,
        caption="👋 Welcome to the Cookie Bot!\nUse /add_cookie and then /run.",
        reply_markup=markup)

@dp.message(Command("add_cookie"))
async def cmd_add_cookie(message: Message):
    if not await check_access(message): return
    cookie = message.text.replace("/add_cookie", "").strip()
    if not cookie:
        await message.answer("❗ Provide a cookie after the command.")
        return
    add_cookie(message.from_user.id, cookie)
    await message.answer("✅ Cookie added.")

@dp.message(Command("delete_cookie"))
async def cmd_delete_cookie(message: Message):
    uid = message.from_user.id
    if not await check_access(message): return
    delete_cookie(uid)
    task = user_tasks.pop(uid, None)
    if task and not task.done():
        task.cancel()
    await message.answer("🗑️ Cookie deleted and loop stopped.")

@dp.message(Command("run"))
async def cmd_run(message: Message):
    uid = message.from_user.id
    if not await check_access(message): return
    if uid in user_tasks:
        await message.answer("⏳ Task already running.")
        return
    cookie = get_cookie(uid)
    if not cookie:
        await message.answer("❗ No cookie found.")
        return
    await message.answer("🔁 Started your request loop. Runs every 15 minutes.")
    task = asyncio.create_task(run_periodic_requests(uid, cookie, message, C_VALUES))
    user_tasks[uid] = task

@dp.message(Command("stop"))
async def cmd_stop(message: Message):
    uid = message.from_user.id
    task = user_tasks.pop(uid, None)
    if task and not task.done():
        task.cancel()
        await message.answer("🛑 Task stopped.")
    else:
        await message.answer("⚠️ No active task.")

@dp.message(Command("status"))
async def cmd_status(message: Message):
    uid = message.from_user.id
    if uid in user_tasks and not user_tasks[uid].done():
        await message.answer("✅ Task is running.")
    else:
        await message.answer("❌ No task running.")

@dp.message(Command("approve"))
async def cmd_approve(message: Message):
    if message.from_user.id not in APPROVED_ADMINS:
        await message.answer("⛔ Only admins can approve users.")
        return
    try:
        uid = int(message.text.replace("/approve", "").strip())
        approve_user(uid)
        await message.answer(f"✅ Approved user {uid}.")
    except ValueError:
        await message.answer("⚠️ Usage: /approve <telegram_user_id>")

@dp.message(Command("list_approved"))
async def cmd_list_approved(message: Message):
    if message.from_user.id not in APPROVED_ADMINS:
        return
    users = list_approved_users()
    await message.answer("✅ Approved users:\n" + "\n".join(map(str, users)))

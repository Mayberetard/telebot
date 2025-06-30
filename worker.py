import asyncio
import httpx
import random

async def run_periodic_requests(user_id, cookie, message, c_values, interval=900):
    headers = {"Cookie": cookie}

    while True:
        sample = random.sample(c_values, 3)
        urls = [f"http://?c={v}" for v in sample]

        async with httpx.AsyncClient() as client:
            results = await asyncio.gather(*[client.get(url, headers=headers) for url in urls])
            for res in results:
                if res.status_code == 200:
                    await message.answer(f"✅ Success: {res.text}")
                else:
                    await message.answer(f"❌ Error: {res.status_code}")

        await asyncio.sleep(interval)  # 15 minutes

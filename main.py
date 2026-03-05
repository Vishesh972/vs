import requests
import asyncio
import threading
from pyrogram import Client, filters, idle
from pyrogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from web import run_flask

# ── Pyrogram setup ──────────────────────────────────────────────
api_id    = 34893727
api_hash  = "ae9e0f5e7ed5b22048e829234b98f503"
bot_token = "8690473371:AAHdD2a-sYRo4V6aHVIQ8WKsKJ63L8sCw_0"

app = Client("my_account", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def my_handler(client: Client, message: Message):
    key = ReplyKeyboardMarkup(
        [[KeyboardButton("Show price")],
         [KeyboardButton("Show summary")]],
        resize_keyboard=True
    )
    await message.reply_text(
        f"Hey, {message.from_user.first_name}!\n\n I am Bitcoin price tracker😎",
        reply_markup=key
    )

@app.on_message(filters.regex("Show price"))
async def price_handler(client: Client, message: Message):
    price = get_price()
    if price:
        await message.reply_text(f"The current price of Bitcoin is: ${price}")
    else:
        await message.reply_text("Failed to fetch the price. Please try again later.")

@app.on_message(filters.regex("Show summary"))
async def summary_handler(client: Client, message: Message):
    data = get_bitcoin_data()
    if data:
        await message.reply_text(format_bitcoin_summary(data))
    else:
        await message.reply_text("Failed to fetch the summary. Please try again later.")

# ── Helpers ─────────────────────────────────────────────────────
def get_bitcoin_data():
    response = requests.get("https://fapi.coinglass.com/api/coin/v2/info?symbol=BTC")
    return response.json() if response.status_code == 200 else None

def get_price():
    data = get_bitcoin_data()
    return data["data"]["price"] if data else None

def format_bitcoin_summary(data):
    btc = data.get("data", {})
    return f"""
🚀 BITCOIN MARKET UPDATE 🚀

💰 Price: ${btc.get('price'):,.2f}
📊 24h Change: {btc.get('priceChangePercent24h')}%
📈 7d Change: {btc.get('priceChangePercent7d')}%

🏦 Market Cap: ${btc.get('marketCap'):,.0f}
🔄 Spot Volume (24h): ${btc.get('volUsd'):,.0f}
⚡ Futures Volume (24h): ${btc.get('futuresVolUsd'):,.0f}

📌 Open Interest: ${btc.get('openInterest'):,.0f}

🪙 Circulating Supply: {btc.get('circulatingSupply'):,.0f} BTC
🔒 Max Supply: {btc.get('maxSupply'):,.0f} BTC

💥 24h Liquidations: ${btc.get('liquidationUsd24h'):,.0f}
📉 Liquidation Positions: {btc.get('liquidationNumber24h'):,}

🔥 Stay sharp. Volatility is opportunity!
"""



# ── Entry point ─────────────────────────────────────────────────
async def main():
    # Start Flask in a background thread
    threading.Thread(target=run_flask, daemon=True).start()
    print("Flask server started on port 5000")

    # Start the Pyrogram bot
    await app.start()
    print("Bot is running")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
import requests
from pyrogram import Client, filters, idle
from pyrogram.types import Message,KeyboardButton,ReplyKeyboardMarkup
import asyncio

api_id = 34893727
api_hash = "ae9e0f5e7ed5b22048e829234b98f503"
bot_token = "8690473371:AAHdD2a-sYRo4V6aHVIQ8WKsKJ63L8sCw_0"
app = Client("my_account", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def my_handler(client : Client, message: Message):
    key=ReplyKeyboardMarkup(
        [
            [KeyboardButton("Show price")],
            [KeyboardButton("Show summary")]
        ],
        resize_keyboard=True
    )
    await message.reply_text(f"Hey, {message.from_user.first_name}!\n\n I am Bitcoin price tracker😎", reply_markup=key)

@app.on_message(filters.regex("Show price"))
async def price_handler(client : Client, message: Message): 
    price=get_price()
    if price:
            await message.reply_text(f"The current price of Bitcoin is: ${price}")
    else:        
        await message.reply_text("failed to fetch the price. Please try again later.")

@app.on_message(filters.regex("Show summary"))
async def summary_handler(client : Client, message: Message): 
    data=get_bitcoin_data()
    if data:
        summary=format_bitcoin_summary(data)
        await message.reply_text(summary)
    else:
        await message.reply_text("failed to fetch the summary. Please try again later.")

def get_bitcoin_data():
    response = requests.get("https://fapi.coinglass.com/api/coin/v2/info?symbol=BTC")
    if(response.status_code==200):
        data=response.json()
        return data
    return None

def get_price():
    response = requests.get("https://fapi.coinglass.com/api/coin/v2/info?symbol=BTC")
    if(response.status_code==200):
        data=response.json()
        price=data["data"]["price"]
        return price
    return None
def format_bitcoin_summary(data):
    btc = data.get("data", {})
    
    price = btc.get("price")
    change_24h = btc.get("priceChangePercent24h")
    change_7d = btc.get("priceChangePercent7d")
    market_cap = btc.get("marketCap")
    volume_spot = btc.get("volUsd")
    volume_futures = btc.get("futuresVolUsd")
    open_interest = btc.get("openInterest")
    circulating = btc.get("circulatingSupply")
    max_supply = btc.get("maxSupply")
    liquidation_24h = btc.get("liquidationUsd24h")
    liquidation_count = btc.get("liquidationNumber24h")

    message = f"""
🚀 BITCOIN MARKET UPDATE 🚀

💰 Price: ${price:,.2f}
📊 24h Change: {change_24h}%
📈 7d Change: {change_7d}%

🏦 Market Cap: ${market_cap:,.0f}
🔄 Spot Volume (24h): ${volume_spot:,.0f}
⚡ Futures Volume (24h): ${volume_futures:,.0f}

📌 Open Interest: ${open_interest:,.0f}

🪙 Circulating Supply: {circulating:,.0f} BTC
🔒 Max Supply: {max_supply:,.0f} BTC

💥 24h Liquidations: ${liquidation_24h:,.0f}
📉 Liquidation Positions: {liquidation_count:,}

🔥 Stay sharp. Volatility is opportunity!
"""
    return message

async def main():
    await app.start()
    print("Bot is running")
    await idle()

if __name__ == "__main__":
        asyncio.run(main())
    
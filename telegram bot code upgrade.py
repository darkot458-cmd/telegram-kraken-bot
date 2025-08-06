# ✅ Fix Pydroid 3 event loop crash + Kraken bot

import logging
import ccxt
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🧠 Patch event loop for Pydroid
import asyncio
import nest_asyncio
nest_asyncio.apply()

# 🔑 Bot token and wallets
BOT_TOKEN = "8324937447:AAFIK-3a23ck14dq0hMbCCz9LcKR7SdFRn8"
USDT_WALLET = "TRNWkLGGfhQsvoDiBCqQLR99gb31y5b7dd"
BTC_WALLET = "bc1qukg87evnj4jfahja6neza0822xlp5t3498m4zm"
balance = {"USDT": 1000, "BTC": 0}

# 🔍 Log config
logging.basicConfig(level=logging.INFO)

# 📍 Bot functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Use /wallet to get deposit address\n"
        "/market to see BTC price\n"
        "/buy to test trade\n"
        "Or send me any message."
    )

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"💼 Wallet Addresses:\n\n"
        f"🪙 USDT (TRC20): `{USDT_WALLET}`\n"
        f"🪙 BTC: `{BTC_WALLET}`",
        parse_mode="Markdown"
    )

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exchange = ccxt.kraken()
    ticker = exchange.fetch_ticker('BTC/USDT')
    price = ticker['last']
    change = ticker.get('percentage', 0)
    direction = "📈 Market is going UP!" if change >= 0 else "📉 Market is going DOWN!"
    await update.message.reply_text(
        f"📊 BTC/USDT: ${price:.2f}\nChange: {change:.2f}%\n{direction}"
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = 10  # $10 trade
    exchange = ccxt.kraken()
    ticker = exchange.fetch_ticker('BTC/USDT')
    price = ticker['last']
    btc_amount = amount / price
    balance["USDT"] -= amount
    balance["BTC"] += btc_amount
    await update.message.reply_text(
        f"✅ Simulated Buy: ${amount} BTC at ${price:.2f}\n"
        f"📊 Balance:\nUSDT: {balance['USDT']:.2f}\nBTC: {balance['BTC']:.6f}"
    )

async def reply_anything(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

# 🚀 Launch bot
async def main():
    print("🤖 Bot is starting...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("wallet", wallet))
    app.add_handler(CommandHandler("market", market))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_anything))

    print("✅ Bot started successfully\n🚀 Polling... (waiting for messages)")
    await app.run_polling()

# ✅ Run using patched loop for Pydroid
asyncio.run(main())
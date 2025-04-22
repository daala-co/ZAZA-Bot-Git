
import os
import telebot
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

portfolio_1 = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT", "DOTUSDT", "LINKUSDT", "LTCUSDT",
    "AVAXUSDT", "MATICUSDT", "FILUSDT", "XLMUSDT", "ATOMUSDT", "HBARUSDT", "GRTUSDT",
    "AAVEUSDT", "APEUSDT", "SANDUSDT", "UNIUSDT", "TAOUSDT", "RNDRUSDT"
]

portfolio_2 = [
    "FETUSDT", "INJUSDT", "RSRUSDT", "JASMYUSDT", "SHIBUSDT", "PEPEUSDT", "ANKRUSDT",
    "CFXUSDT", "VANAUSDT", "BRETTUSDT", "BONKUSDT", "ARKMUSDT", "BICOUSDT", "IMXUSDT",
    "MOVEUSDT", "BEAMXUSDT", "AUDIOUSDT", "PENGUUSDT", "FLOKIUSDT", "TRUMPUSDT"
]

def get_token_name(symbol):
    names = {
        "BTCUSDT": "Bitcoin", "ETHUSDT": "Ethereum", "SOLUSDT": "Solana", "ADAUSDT": "Cardano",
        "DOTUSDT": "Polkadot", "LINKUSDT": "Chainlink", "LTCUSDT": "Litecoin", "AVAXUSDT": "Avalanche",
        "MATICUSDT": "Polygon", "FILUSDT": "Filecoin", "XLMUSDT": "Stellar", "ATOMUSDT": "Cosmos",
        "HBARUSDT": "Hedera", "GRTUSDT": "The Graph", "AAVEUSDT": "Aave", "APEUSDT": "ApeCoin",
        "SANDUSDT": "The Sandbox", "UNIUSDT": "Uniswap", "TAOUSDT": "Bittensor", "RNDRUSDT": "Render",
        "FETUSDT": "Fetch.ai", "INJUSDT": "Injective", "RSRUSDT": "Reserve Rights", "JASMYUSDT": "JasmyCoin",
        "SHIBUSDT": "SHIBA INU", "PEPEUSDT": "Pepe", "ANKRUSDT": "Ankr", "CFXUSDT": "Conflux",
        "VANAUSDT": "Vana", "BRETTUSDT": "Brett", "BONKUSDT": "Bonk", "ARKMUSDT": "Arkham",
        "BICOUSDT": "Biconomy", "IMXUSDT": "Immutable X", "MOVEUSDT": "Movement", "BEAMXUSDT": "Beam",
        "AUDIOUSDT": "Audius", "PENGUUSDT": "Pudgy Penguins", "FLOKIUSDT": "Floki", "TRUMPUSDT": "Trump"
    }
    return names.get(symbol, symbol)

def format_price(symbol, price, change):
    arrow = "📈" if float(change) > 0 else "📉"
    color = "🟢" if float(change) > 0 else "🔴"
    return f"{arrow} {price} {color} ({change}%)"

def build_line(symbol, rsi, macd_status, trend_status, action, price, change):
    token_name = get_token_name(symbol)
    price_info = format_price(symbol, price, change)
    return f"*{token_name}* ({symbol})\n→ RSI {rsi:.2f} | {macd_status} | {trend_status} | {price_info} | {action}\n"

# Commandes de simulation Telegram
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "🤖 Bot actif. Utilise /P1, /P2 ou /tot pour voir ton portefeuille.")

@bot.message_handler(commands=['P1'])
def handle_p1(message):
    text = "*📊 Portefeuille 1 :*
"
    for symbol in portfolio_1:
        line = build_line(symbol, 50, "MACD 🔽", "MA50 📉", "🔍 Surveillance", "50.23$", "-2.5")
        text += line + "\n"
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['P2'])
def handle_p2(message):
    text = "*📊 Portefeuille 2 :*
"
    for symbol in portfolio_2:
        line = build_line(symbol, 45, "MACD 🔼", "MA200 📈", "🟢 Achat", "0.023$", "+8.1")
        text += line + "\n"
    bot.reply_to(message, text, parse_mode="Markdown")

bot.polling()

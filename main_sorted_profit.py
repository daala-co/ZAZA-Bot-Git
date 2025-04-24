
import os
import telebot
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Token Telegram et clés API Binance
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

bot = telebot.TeleBot(BOT_TOKEN)
client = Client(API_KEY, API_SECRET)

# Portefeuilles
portfolio1 = {
    "BTC": 0.26697, "ETH": 1.527, "SOL": 49.26, "ADA": 5040, "DOT": 654.2,
    "LINK": 290.2, "LTC": 26.7, "XRP": 10224.23, "DOGE": 112340, "AVAX": 88,
    "RNDR": 456.87, "ATOM": 152.1, "UNI": 230, "MATIC": 1255, "GRT": 14450,
    "FIL": 1020, "ALGO": 4120, "HBAR": 7852, "APE": 386.2, "SAND": 1272,
    "XLM": 11842, "TAO": 1.1, "INJ": 12.3, "FET": 432, "CKB": 14520, "KAS": 2150,
    "RSR": 18340, "JASMY": 28500, "SHIB": 11580000, "PEPE": 23500000,
    "VIRTUAL": 1842, "ANKR": 4900, "CFX": 2800, "VANA": 370, "BRETT": 125400,
    "BONK": 1900000, "ARKM": 125, "BICO": 215, "PENGU": 50, "MOVE": 80,
    "BEAMX": 300, "ATH": 215, "FLOKI": 1080000
}

portfolio2 = {
    "TRUMP": 120, "AUDIO": 530, "IMX": 420
}

# Utilitaires
def get_token_name(symbol):
    mapping = {
        "BTC": "Bitcoin", "ETH": "Ethereum", "SOL": "Solana", "ADA": "Cardano",
        "DOT": "Polkadot", "LINK": "Chainlink", "LTC": "Litecoin", "XRP": "Ripple",
        "DOGE": "Dogecoin", "AVAX": "Avalanche", "RNDR": "Render", "ATOM": "Cosmos",
        "UNI": "Uniswap", "MATIC": "Polygon", "GRT": "The Graph", "FIL": "Filecoin",
        "ALGO": "Algorand", "HBAR": "Hedera", "APE": "ApeCoin", "SAND": "Sandbox",
        "XLM": "Stellar", "TAO": "Bittensor", "INJ": "Injective", "FET": "Fetch.ai",
        "CKB": "Nervos", "KAS": "Kaspa", "RSR": "Reserve Rights", "JASMY": "Jasmy",
        "SHIB": "Shiba Inu", "PEPE": "Pepe", "VIRTUAL": "Virtuals", "ANKR": "Ankr",
        "CFX": "Conflux", "VANA": "Vana", "BRETT": "Brett", "BONK": "Bonk",
        "ARKM": "Arkham", "BICO": "Biconomy", "PENGU": "Pudgy Penguins",
        "MOVE": "Movement", "BEAMX": "Beam", "ATH": "Aethir", "FLOKI": "Floki",
        "TRUMP": "Trump", "AUDIO": "Audius", "IMX": "ImmutableX"
    }
    return mapping.get(symbol, symbol)

def format_price(price, percent):
    price = float(price)
    percent = float(percent)
    emoji = "🟢" if percent > 0 else "🔴" if percent < 0 else "⚪️"
    return f"`{price:.4f}` USD {emoji} ({percent:.2f}%)"

def get_price(symbol):
    try:
        data = client.get_ticker(symbol=f"{symbol}USDT")
        return float(data['lastPrice']), float(data['priceChangePercent'])
    except BinanceAPIException:
        return 0.0, 0.0

def build_portfolio_summary(portfolio):
    summaries = []
    for sym, qty in portfolio.items():
        price, percent = get_price(sym)
        total = price * qty
        summaries.append((sym, qty, price, percent, total))
    summaries.sort(key=lambda x: x[4], reverse=True)
    return summaries

def build_portfolio_text(portfolio, name):
    summary = build_portfolio_summary(portfolio)
    text = f"*📦 Portefeuille {name}*

"
    for sym, qty, price, percent, total in summary:
        price_str = format_price(price, percent)
        name_str = get_token_name(sym)
        gain_loss = "✅" if percent > 0 else "🔻" if percent < 0 else "⚪️"
        text += f"*{name_str} ({sym}USDT)*
💰 {qty} {sym} ≈ `${total:,.2f}` USD {gain_loss}
Prix : {price_str}

"
    return text

# Handlers
@bot.message_handler(commands=['P1'])
def send_p1(message):
    text = build_portfolio_text(portfolio1, "1")
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['P2'])
def send_p2(message):
    text = build_portfolio_text(portfolio2, "2")
    bot.reply_to(message, text, parse_mode="Markdown")

bot.polling()

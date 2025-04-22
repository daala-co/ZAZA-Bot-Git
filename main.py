import os
import requests
import telebot

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

portfolio_1 = [
    "BTCUSDT", "ETHUSDT", "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "APEUSDT", "ATOMUSDT",
    "DOGEUSDT", "DOTUSDT", "FILUSDT", "GRTUSDT", "HBARUSDT", "LINKUSDT", "LTCUSDT",
    "ONDOUSDT", "POLUSDT", "RNDRUSDT", "SANDUSDT", "SOLUSDT", "UNIUSDT", "XLMUSDT", "XRPUSDT"
]

symbol_to_name = {
    "BTCUSDT": "Bitcoin", "ETHUSDT": "Ethereum", "AAVEUSDT": "Aave", "ADAUSDT": "Cardano",
    "ALGOUSDT": "Algorand", "APEUSDT": "ApeCoin", "ATOMUSDT": "Cosmos", "DOGEUSDT": "Dogecoin",
    "DOTUSDT": "Polkadot", "FILUSDT": "Filecoin", "GRTUSDT": "The Graph", "HBARUSDT": "Hedera",
    "LINKUSDT": "Chainlink", "LTCUSDT": "Litecoin", "ONDOUSDT": "Ondo", "POLUSDT": "Polygon",
    "RNDRUSDT": "Render", "SANDUSDT": "The Sandbox", "SOLUSDT": "Solana", "UNIUSDT": "Uniswap",
    "XLMUSDT": "Stellar", "XRPUSDT": "Ripple"
}

holdings_chf = {
    "ETHUSDT": 15659.19, "BTCUSDT": 18817.65, "XRPUSDT": 9484.97, "SOLUSDT": 4885.52,
    "ONDOUSDT": 2525.24, "ADAUSDT": 1179.07, "DOGEUSDT": 1121.80, "ATOMUSDT": 910.56,
    "HBARUSDT": 613.84, "APEUSDT": 508.31, "AAVEUSDT": 455.22, "LINKUSDT": 439.98,
    "RNDRUSDT": 816.88, "POLUSDT": 391.01, "ALGOUSDT": 185.43, "DOTUSDT": 154.53,
    "FILUSDT": 242.15, "UNIUSDT": 220.84, "SANDUSDT": 219.85, "PEPEUSDT": 209.44,
    "GRTUSDT": 60.78, "LTCUSDT": 62.63, "XLMUSDT": 84.72, "USDT": 80.00
}

def get_crypto_data(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    try:
        response = requests.get(url).json()
        price = float(response["lastPrice"])
        percent = float(response["priceChangePercent"])
        return price, percent
    except:
        return None, None

def format_price(price, percent):
    if price is None:
        return "❌ Données indisponibles"
    arrow = "🔻" if percent < 0 else "🔺"
    color = "🔴" if percent < 0 else "🟢"
    return f"{arrow} {price:.4f} USD ({color} {percent:.2f}%)"

def get_analysis(symbol):
    price, percent = get_crypto_data(symbol)
    rsi = 50 + (hash(symbol) % 50 - 25)
    macd_pos = hash(symbol) % 2 == 0

    if rsi >= 70:
        rsi_status = "🔴 Surachat"
        action = "🛑 Vente"
    elif rsi <= 30:
        rsi_status = "🟢 Survente"
        action = "🟩 Achat"
    else:
        rsi_status = "🟡 RSI neutre"
        action = "🔍 Surveillance"

    macd_status = "📉 MACD négatif" if not macd_pos else "📈 MACD positif"
    trend_status = "📊 Tendance neutre"
    price_info = format_price(price, percent)
    token_name = symbol_to_name.get(symbol, symbol.replace("USDT", ""))

    variation = ""
    if symbol in holdings_chf:
        variation = f"(CHF {holdings_chf[symbol]:,.2f})"

    return f"*{token_name} ({symbol})* – 💰 {variation}\n{price_info}\nRSI {rsi:.2f} | {rsi_status} | {macd_status} | {trend_status} | {action}\n"

def build_message(title, portfolio):
    ordered = sorted(portfolio, key=lambda s: -holdings_chf.get(s, 0))
    text = f"📦 *{title} – Analyse Complète*\n\n"
    for symbol in ordered:
        text += get_analysis(symbol) + "\n"
    return text

@bot.message_handler(commands=["P1"])
def handle_p1(message):
    msg = build_message("Portefeuille 1", portfolio_1)
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

bot.polling()
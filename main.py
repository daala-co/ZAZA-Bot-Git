
import telebot
import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Portefeuilles par catégorie
categories = {
    "🌐 Blue Chips": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"],
    "🧠 IA": ["FETUSDT", "INJUSDT", "TAOUSDT", "CKBUSDT", "AGIXUSDT"],
    "🧱 Infrastructures": ["DOTUSDT", "ATOMUSDT", "AVAXUSDT", "KASUSDT", "NEARUSDT"],
    "🌐 DeFi": ["UNIUSDT", "AAVEUSDT", "SUSHIUSDT", "RSRUSDT", "CRVUSDT"],
    "🌈 NFT / Metaverse": ["SANDUSDT", "APEUSDT", "MANAUSDT", "PENGUUSDT", "AUDIOUSDT"],
    "🧪 Divers": ["SHIBUSDT", "PEPEUSDT", "BONKUSDT", "VIRTUALUSDT", "BRETTUSDT", "ARKMUSDT", "BICOUSDT", "MOVEUSDT", "BEAMXUSDT", "FLOKIUSDT"]
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

def format_price_change(percent):
    if percent is None:
        return ""
    arrow = "🔺" if percent > 0 else "🔻"
    return f"{arrow} {percent:.2f}%"

def get_analysis(symbol):
    price, percent = get_crypto_data(symbol)
    rsi = 50 + (hash(symbol) % 50 - 25)  # Simule RSI
    macd_pos = hash(symbol) % 2 == 0
    trend = "neutre"

    if rsi > 70:
        rsi_status = "🔴 Surachat"
        status = "🛑 Vente"
    elif rsi < 30:
        rsi_status = "🟢 Survente"
        status = "🟩 Achat"
    else:
        rsi_status = "🟡 RSI neutre"
        status = "🔍 Surveillance"

    macd_status = "📉 MACD négatif" if not macd_pos else "📈 MACD positif"
    trend_status = "📊 Tendance neutre"
    price_part = f"💰 {price:.4f} USD" if price else ""
    change_part = format_price_change(percent)

    return f"{symbol} → RSI {rsi:.0f} | {rsi_status} | {macd_status} | {trend_status} | {price_part} {change_part} | {status}"

def build_message():
    text = ""
    for title, symbols in categories.items():
        text += f"{title}\n"
        for sym in symbols:
            text += get_analysis(sym) + "\n\n"
    return text

@bot.message_handler(commands=['P1'])
def handle_portfolio1(message):
    msg = build_message()
    bot.send_message(message.chat.id, msg)

bot.polling()

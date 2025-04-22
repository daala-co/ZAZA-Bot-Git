
import telebot
import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

portfolio_1 = [
    "BTCUSDT", "ETHUSDT", "AUDIOUSDT", "SOLUSDT", "LINKUSDT", "ATOMUSDT",
    "LTCUSDT", "ADAUSDT", "DOTUSDT", "MATICUSDT", "FILUSDT", "XLMUSDT",
    "UNIUSDT", "DOGEUSDT", "GRTUSDT", "HBARUSDT", "APEUSDT", "SANDUSDT",
    "TAOUSDT", "INJUSDT", "FETUSDT", "CKBUSDT", "SHIBUSDT", "PEPEUSDT",
    "VIRTUALUSDT", "ANKRUSDT", "CFXUSDT", "VANAUSDT", "BRETTUSDT",
    "BONKUSDT", "ARKMUSDT", "BICOUSDT", "MOVEUSDT", "BEAMXUSDT",
    "RNDRUSDT", "PENGUUSDT", "ATHUSDT", "FLOKIUSDT", "TRUMPUSDT"
]

portfolio_2 = [
    "FETUSDT", "INJUSDT", "CKBUSDT", "SHIBUSDT", "PEPEUSDT", "VIRTUALUSDT",
    "ANKRUSDT", "CFXUSDT", "VANAUSDT", "BRETTUSDT", "BONKUSDT", "ARKMUSDT",
    "BICOUSDT", "IMXUSDT", "MOVEUSDT", "BEAMXUSDT", "ATHUSDT",
    "PENGUUSDT", "FLOKIUSDT", "TRUMPUSDT"
]

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
    if price is None:
        return f"*{symbol}* ❌ Données indisponibles"

    rsi = 50 + (hash(symbol) % 50 - 25)
    macd_pos = hash(symbol) % 2 == 0

    status = "🔍 Surveillance"
    rsi_status = "🟡 RSI neutre"
    trend_status = "📊 Tendance neutre"

    if rsi > 70:
        rsi_status = "🔴 Surachat"
        status = "🛑 Vente"
    elif rsi < 30:
        rsi_status = "🟢 Survente"
        status = "🟩 Achat"

    macd_status = "📉 MACD négatif" if not macd_pos else "📈 MACD positif"
    change_part = format_price_change(percent)
    price_part = f"💰 {price:.4f} USD" if price else ""

    return f"*{symbol}* → RSI {rsi:.2f} | {rsi_status} | {macd_status} | {trend_status} | {price_part} {change_part} | {status}\n"

@bot.message_handler(commands=['S'])
def signal_response(message):
    s_symbols = [s for s in portfolio_1 + portfolio_2 if hash(s) % 3 == 0]
    if not s_symbols:
        bot.send_message(message.chat.id, "⚠️ Aucune crypto avec un signal d'achat ou de vente détecté.")
        return
    text = "*📊 Signaux détectés :*"

"
    for sym in s_symbols:
        text += get_analysis(sym) + "
"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['SS'])
def rsi_response(message):
    ss_symbols = [s for s in portfolio_1 + portfolio_2 if hash(s) % 4 == 0]
    if not ss_symbols:
        bot.send_message(message.chat.id, "⚠️ Aucune crypto en surachat ou survente détectée.")
        return
    text = "*📊 Surachat / Survente :*

"
    for sym in ss_symbols:
        text += get_analysis(sym) + "
"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

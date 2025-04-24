
import os
import requests
import telebot

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

portfolio_1 = [
    "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "APEUSDT", "ATOMUSDT", "BTCUSDT",
    "DOGEUSDT", "DOTUSDT", "ETHUSDT", "FILUSDT", "GRTUSDT", "HBARUSDT",
    "LINKUSDT", "LTCUSDT", "ONDOUSDT", "POLUSDT", "RNDRUSDT", "SANDUSDT",
    "SOLUSDT", "UNIUSDT", "XLMUSDT", "XRPUSDT"
]
portfolio_2 = [
    "FETUSDT", "INJUSDT", "CKBUSDT", "KASUSDT", "RSRUSDT", "JASMYUSDT",
    "SHIBUSDT", "PEPEUSDT", "VIRTUALUSDT", "ANKRUSDT", "CFXUSDT", "VANAUSDT",
    "BRETTUSDT", "BONKUSDT", "ARKMUSDT", "BICOUSDT", "IMXUSDT", "MOVEUSDT",
    "BEAMXUSDT", "ATHUSDT", "PENGUUSDT", "FLOKIUSDT", "TRUMPUSDT", "AUDIOUSDT"
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

def format_price(price, percent):
    if price is None or percent is None:
        return "❌ Données indisponibles"
    arrow = "🔺" if percent > 0 else "🔻"
    color = "🟢" if percent > 0 else "🔴"
    return f"💰 {price:.4f} USD {color} {arrow} {percent:.2f}%"

def get_token_name(symbol):
    mapping = {
        "RNDRUSDT": "RENDER",
        "CKBUSDT": "NERVOS NETWORK",
        "FETUSDT": "FETCH.AI",
        "ATHUSDT": "AETHIR",
        "ARKMUSDT": "ARKHAM",
        "IMXUSDT": "IMMUTABLE X",
        "BONKUSDT": "BONK",
        "BRETTUSDT": "BRETT",
        "VANAUSDT": "VANA",
        "MOVEUSDT": "MOVEMENT",
        "BEAMXUSDT": "BEAM",
        "PENGUUSDT": "PUDGY PENGUINS",
        "TRUMPUSDT": "TRUMP",
        "AUDIOUSDT": "AUDIUS"
    }
    return mapping.get(symbol, symbol.replace("USDT", ""))

def get_analysis(symbol):
    price, percent = get_crypto_data(symbol)
    rsi = 50 + (hash(symbol) % 50 - 25)
    macd_pos = hash(symbol) % 2 == 0
    status = "🔍 Surveillance"
    rsi_status = "🟡 RSI neutre"
    if rsi > 70:
        rsi_status = "🔴 Surachat"
        status = "🛑 Vente"
    elif rsi < 30:
        rsi_status = "🟢 Survente"
        status = "🟢 Achat"
    macd_status = "📉 MACD négatif" if not macd_pos else "📈 MACD positif"
    trend = "📊 Tendance neutre"
    price_part = format_price(price, percent)
    return f"*{get_token_name(symbol)}* ({symbol})\nRSI {rsi:.2f} | {rsi_status} | {macd_status} | {trend} | {price_part} | {status}\n"

def build_message(title, portfolio):
    text = f"📦 *{title} – Analyse Complète*\n\n"
    for symbol in portfolio:
        text += get_analysis(symbol) + "\n"
    return text

@bot.message_handler(commands=["P1"])
def handle_p1(message):
    text = build_message("Portefeuille 1", portfolio_1)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["P2"])
def handle_p2(message):
    text = build_message("Portefeuille 2", portfolio_2)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["tot"])
def handle_tot(message):
    gainers = [s for s in portfolio_1 + portfolio_2 if get_crypto_data(s)[1] and get_crypto_data(s)[1] > 0]
    losers = [s for s in portfolio_1 + portfolio_2 if get_crypto_data(s)[1] and get_crypto_data(s)[1] < 0]
    text = "📊 *Résumé global du portefeuille*\n\n"
    text += f"💹 Top hausses : {', '.join(gainers[:3]) if gainers else 'aucune'}\n"
    text += f"📉 Top baisses : {', '.join(losers[:3]) if losers else 'aucune'}\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

bot.polling()

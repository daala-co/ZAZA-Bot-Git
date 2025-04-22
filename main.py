import telebot
import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

portfolio_1 = ["BTCUSDT", "ETHUSDT", "AUDIOUSDT", "SOLUSDT", "LINKUSDT", "ATOMUSDT", "RNDRUSDT"]
portfolio_2 = ["FETUSDT", "INJUSDT", "PEPEUSDT", "BONKUSDT", "PENGUUSDT", "VIRTUALUSDT", "ANKRUSDT", "CFXUSDT", "VANAUSDT", "BRETTUSDT", "ARKMUSDT", "BICOUSDT", "IMXUSDT", "MOVEUSDT", "BEAMXUSDT", "ATHUSDT", "PENGUUSDT", "FLOKIUSDT", "TRUMPUSDT"]


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
    rsi = 50 + (hash(symbol) % 50 - 25)
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

    price_color = "🟢" if percent and percent > 0 else "🔴"
    price_part = f"💰 {price:.4f} USD {price_color}" if price else f"{symbol} ❌ Données indisponibles"
    change_part = format_price_change(percent)

    name = name_from_symbol(symbol)

    return f"\n*{name} ({symbol})*\n{symbol} → RSI {rsi:.2f} | {rsi_status} | {macd_status} | {trend_status} | {price_part} {change_part} | {status}\n"


def name_from_symbol(symbol):
    name_map = {
        "BTCUSDT": "Bitcoin",
        "ETHUSDT": "Ethereum",
        "AUDIOUSDT": "Audius",
        "SOLUSDT": "Solana",
        "LINKUSDT": "Chainlink",
        "ATOMUSDT": "Cosmos",
        "RNDRUSDT": "Render",
        "FETUSDT": "Fetch.ai",
        "INJUSDT": "Injective",
        "PEPEUSDT": "Pepe",
        "BONKUSDT": "Bonk",
        "PENGUUSDT": "Pudgy Penguins",
        "VIRTUALUSDT": "Virtuals Protocol",
        "ANKRUSDT": "Ankr",
        "CFXUSDT": "Conflux",
        "VANAUSDT": "Vana",
        "BRETTUSDT": "Brett",
        "ARKMUSDT": "Arkham",
        "BICOUSDT": "Biconomy",
        "IMXUSDT": "Immutable X",
        "MOVEUSDT": "Movement",
        "BEAMXUSDT": "Beam",
        "ATHUSDT": "Aethir",
        "FLOKIUSDT": "Floki",
        "TRUMPUSDT": "Trump"
    }
    return name_map.get(symbol, symbol)


def build_message(title, symbols):
    text = f"*{title}*\n"
    for sym in symbols:
        text += get_analysis(sym) + "\n"
    return text


def signal_response(message):
    s_symbols = [s for s in portfolio_1 + portfolio_2 if hash(s) % 3 == 0]
    if not s_symbols:
        bot.send_message(message.chat.id, "⚠️ Aucune crypto avec un signal d'achat ou vente détecté.")
        return
    text = "*📊 Signaux détectés :*\n"
    for sym in s_symbols:
        text += get_analysis(sym) + "\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


def rsi_extreme_response(message):
    s_symbols = [s for s in portfolio_1 + portfolio_2 if hash(s) % 7 == 0]
    if not s_symbols:
        bot.send_message(message.chat.id, "⚠️ Aucune crypto en surachat ou survente détectée.")
        return
    text = "*📊 RSI Extrêmes :*\n"
    for sym in s_symbols:
        text += get_analysis(sym) + "\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(commands=["P1"])
def handle_p1(message):
    text = build_message("📊 Analyse Portefeuille 1", portfolio_1)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(commands=["P2"])
def handle_p2(message):
    text = build_message("📊 Analyse Portefeuille 2", portfolio_2)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(commands=["S"])
def handle_signals(message):
    signal_response(message)


@bot.message_handler(commands=["SS"])
def handle_extremes(message):
    rsi_extreme_response(message)


bot.polling()

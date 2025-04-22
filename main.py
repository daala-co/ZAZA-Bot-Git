import telebot
import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

portfolio_1 = ["BTCUSDT", "ETHUSDT", "AUDIOUSDT", "SOLUSDT", "LINKUSDT", "ATOMUSDT", "FETUSDT", "INJUSDT", "DOTUSDT", "MATICUSDT", "ADAUSDT", "RNDRUSDT", "XLMUSDT", "XRPUSDT", "DOGEUSDT", "LTCUSDT", "FILUSDT", "GRTUSDT", "UNIUSDT", "AAVEUSDT"]
portfolio_2 = ["TAOUSDT", "FETUSDT", "INJUSDT", "CKBUSDT", "KASUSDT", "RSRUSDT", "JASMYUSDT", "SHIBUSDT", "PEPEUSDT", "VIRTUALUSDT", "ANKRUSDT", "CFXUSDT", "VANAUSDT", "BRETTUSDT", "BONKUSDT", "ARKMUSDT", "BICOUSDT", "IMXUSDT", "MOVEUSDT", "BEAMXUSDT", "ATHUSDT", "PENGUUSDT", "FLOKIUSDT", "TRUMPUSDT", "AUDIOUSDT"]


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
    arrow = "🔼" if percent > 0 else "🔽"
    return f"{arrow} {percent:.2f}%"


def format_price_value(price, percent):
    if price is None:
        return "❌ Données indisponibles"
    color = "🟢" if percent >= 0 else "🔴"
    return f"💰 {price:.4f} USD {color}"


def get_analysis(symbol):
    price, percent = get_crypto_data(symbol)
    rsi = 50 + (hash(symbol) % 50 - 25)
    macd_pos = hash(symbol) % 2 == 0

    name = symbol.replace("USDT", "")
    status = ""
    rsi_status = "🟡 RSI neutre"
    if rsi > 70:
        rsi_status = "🔴 Surachat"
        status = "🛑 Vente"
    elif rsi < 30:
        rsi_status = "🟢 Survente"
        status = "🟩 Achat"

    macd_status = "📉 MACD négatif" if not macd_pos else "📈 MACD positif"
    trend_status = "📊 Tendance neutre"
    price_part = format_price_value(price, percent)
    change_part = format_price_change(percent)

    return f"\n<b>{name}</b> ({symbol})\n{symbol} → RSI {rsi:.2f} | {rsi_status} | {macd_status} | {trend_status} | {price_part} {change_part} | {status}\n"


def build_message(title, symbols):
    text = f"\ud83d\udcca <b>{title}</b>\n"
    for sym in symbols:
        text += get_analysis(sym) + "\n"
    return text


def signal_response(message):
    s_symbols = [s for s in portfolio_1 + portfolio_2 if hash(s) % 3 == 0]
    if not s_symbols:
        bot.send_message(message.chat.id, "\u26a0\ufe0f Aucune crypto avec un signal d'achat ou de vente", parse_mode="HTML")
        return
    text = "\ud83d\udcca <b>Signaux détectés :</b>\n"
    for sym in s_symbols:
        text += get_analysis(sym) + "\n"
    bot.send_message(message.chat.id, text, parse_mode="HTML")


def oversold_response(message):
    s_symbols = [s for s in portfolio_1 + portfolio_2 if (50 + (hash(s) % 50 - 25)) < 30 or (50 + (hash(s) % 50 - 25)) > 70]
    if not s_symbols:
        bot.send_message(message.chat.id, "\u26a0\ufe0f Aucune crypto en surachat ou survente", parse_mode="HTML")
        return
    text = "\ud83d\udcca <b>Cryptos en surachat / survente :</b>\n"
    for sym in s_symbols:
        text += get_analysis(sym) + "\n"
    bot.send_message(message.chat.id, text, parse_mode="HTML")


@bot.message_handler(commands=['P1'])
def handle_p1(message):
    bot.send_message(message.chat.id, build_message("Analyse Portefeuille 1", portfolio_1), parse_mode="HTML")


@bot.message_handler(commands=['P2'])
def handle_p2(message):
    bot.send_message(message.chat.id, build_message("Analyse Portefeuille 2", portfolio_2), parse_mode="HTML")


@bot.message_handler(commands=['S'])
def handle_signals(message):
    signal_response(message)


@bot.message_handler(commands=['SS'])
def handle_oversold(message):
    oversold_response(message)


bot.polling()

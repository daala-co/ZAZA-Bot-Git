import telebot
import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Portefeuille 1
categories = {
    "Blue Chips": ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT", "SOLUSDT", "LTCUSDT", "XRPUSDT", "XLMUSDT"],
    "DeFi & Finance": ["UNIUSDT", "AAVEUSDT", "LINKUSDT", "FILUSDT", "ATOMUSDT", "HBARUSDT"],
    "AI & Data": ["GRTUSDT"],
    "NFT / Gaming": ["SANDUSDT", "APEUSDT"],
    "Divers / Autres": ["ALGOUSDT", "DOGEUSDT", "ONDOUSDT", "POLUSDT", "VIRTUALUSDT", "MOVEUSDT"]
}

# Portefeuille 2
categories_P2 = {
    "AI & Data": ["TAOUSDT", "INJUSDT", "FETUSDT", "RSRUSDT", "JASMYUSDT", "VANAUSDT", "ARKMUSDT"],
    "Infra & Layer 1/2": ["CKBUSDT", "KASUSDT", "CFXUSDT", "ANKRUSDT", "BEAMXUSDT", "BICOUSDT", "ATHUSDT"],
    "Meme & Fun": ["PEPEUSDT", "SHIBUSDT", "BONKUSDT", "BRETTUSDT", "PENGUUSDT", "TRUMPUSDT"],
    "NFT / Gaming": ["AUDIOUSDT"]
}

def get_crypto_data(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        data = requests.get(url).json()
        price = float(data["lastPrice"])
        percent = float(data["priceChangePercent"])
        return price, percent
    except:
        return None, None

def format_price_change(percent):
    if percent is None:
        return ""
    arrow = "🔺" if percent > 0 else "🔻"
    return f"{arrow} {percent:.2f}%"

def format_price(price, percent):
    if price is None:
        return ""
    color = "🟢" if percent > 0 else "🔴" if percent < 0 else "➖"
    return f"{color} {price:.4f} USD"

def get_analysis(symbol):
    price, percent = get_crypto_data(symbol)
    rsi = 50 + (hash(symbol) % 50 - 25)
    macd_pos = hash(symbol) % 2 == 0

    if rsi > 70:
        rsi_status = "🔴 Surachat"
        signal = "🛑 Vente"
    elif rsi < 30:
        rsi_status = "🟢 Survente"
        signal = "🟩 Achat"
    else:
        rsi_status = "🟡 RSI neutre"
        signal = "🔍 Surveillance"

    macd_status = "📈 MACD positif" if macd_pos else "📉 MACD négatif"
    trend_status = "📊 Tendance neutre"
    price_str = format_price(price, percent)
    change_str = format_price_change(percent)

    full_text = f"{symbol} → RSI {rsi} | {rsi_status} | {macd_status} | {trend_status} | {price_str} {change_str} | {signal}\n"
    return full_text, signal, rsi_status

def build_response(cats):
    text = ""
    for title, symbols in cats.items():
        text += f"\n📦 *{title}*\n"
        for sym in symbols:
            res, _, _ = get_analysis(sym)
            text += res + "\n"
    return text

@bot.message_handler(commands=['P1'])
def handle_P1(message):
    msg = build_response(categories)
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

@bot.message_handler(commands=['P2'])
def handle_P2(message):
    msg = build_response(categories_P2)
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

@bot.message_handler(commands=['SS'])
def handle_SS(message):
    text = "📉 *Crypto en Surachat / Survente*\n"
    for sym_list in list(categories.values()) + list(categories_P2.values()):
        for sym in sym_list:
            result, _, rsi_status = get_analysis(sym)
            if "Surachat" in rsi_status or "Survente" in rsi_status:
                text += result + "\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['S'])
def handle_S(message):
    text = "📢 *Crypto avec Signal Achat ou Vente*\n"
    for sym_list in list(categories.values()) + list(categories_P2.values()):
        for sym in sym_list:
            result, signal, _ = get_analysis(sym)
            if "Achat" in signal or "Vente" in signal:
                text += result + "\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

bot.polling()

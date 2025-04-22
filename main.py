import os
import requests
import telebot

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

portfolio_1 = [
    ("Bitcoin", "BTCUSDT"),
    ("Ethereum", "ETHUSDT"),
    ("Audius", "AUDIOUSDT"),
    ("Solana", "SOLUSDT"),
    ("Chainlink", "LINKUSDT"),
    ("Cosmos", "ATOMUSDT"),
    ("Cardano", "ADAUSDT"),
    ("Polygon", "MATICUSDT"),
    ("Polkadot", "DOTUSDT"),
    ("Render", "RNDRUSDT")
]

portfolio_2 = [
    ("Bittensor", "TAOUSDT"),
    ("Injective", "INJUSDT"),
    ("Fetch.ai", "FETUSDT"),
    ("Nervos Network", "CKBUSDT"),
    ("Kaspa", "KASUSDT"),
    ("Reserve Rights", "RSRUSDT"),
    ("JasmyCoin", "JASMYUSDT"),
    ("Shiba Inu", "SHIBUSDT"),
    ("Pepe", "PEPEUSDT"),
    ("Virtuals", "VIRTUALUSDT"),
    ("Ankr", "ANKRUSDT"),
    ("Conflux", "CFXUSDT"),
    ("Vana", "VANAUSDT"),
    ("Brett", "BRETTUSDT"),
    ("Bonk", "BONKUSDT"),
    ("Arkham", "ARKMUSDT"),
    ("Biconomy", "BICOUSDT"),
    ("Immutable X", "IMXUSDT"),
    ("Movement", "MOVEUSDT"),
    ("Beam", "BEAMXUSDT"),
    ("Aethir", "ATHUSDT"),
    ("Pudgy Penguins", "PENGUUSDT"),
    ("Floki", "FLOKIUSDT"),
    ("Trump", "TRUMPUSDT"),
    ("Audius", "AUDIOUSDT")
]

def get_crypto_data(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    try:
        response = requests.get(url).json()
        price = float(response['lastPrice'])
        change = float(response['priceChangePercent'])
        return price, change
    except:
        return None, None

def get_analysis(name, symbol):
    price, change = get_crypto_data(symbol)
    rsi = 50 + (hash(symbol) % 50 - 25)  # Simulation
    macd_positive = hash(symbol) % 2 == 0

    rsi_status = "🟡 RSI neutre"
    action = "🔍 Surveillance"
    if rsi >= 70:
        rsi_status = "🔴 Surachat"
        action = "🛑 Vente"
    elif rsi <= 30:
        rsi_status = "🟢 Survente"
        action = "🟩 Achat"

    macd_status = "📉 MACD négatif" if not macd_positive else "📈 MACD positif"
    trend = "📊 Tendance neutre"

    if price is None:
        return f"*{name}* ({symbol})\n{symbol} ❌ Données indisponibles\n"

    price_color = "🟢" if change >= 0 else "🔴"
    change_str = f"{price_color} {change:.2f}%"
    return (
        f"*{name}* ({symbol})\n"
        f"{symbol} → RSI {rsi:.2f} | {rsi_status} |\n"
        f"{macd_status} | {trend} |\n"
        f"💰 {price:.4f} USD {change_str} | {action}\n"
    )

def build_message(title, portfolio):
    text = f"\U0001F4CA *{title}*\n\n"
    for name, symbol in portfolio:
        text += get_analysis(name, symbol) + "\n"
    return text

def filter_signals(portfolio):
    return [x for x in portfolio if hash(x[1]) % 3 == 0]

def signal_response(message):
    s_symbols = filter_signals(portfolio_1 + portfolio_2)
    if not s_symbols:
        bot.send_message(message.chat.id, "⚠️ Aucune crypto avec un signal d'achat ou de vente clair.")
        return
    text = "*📊 Signaux détectés :*\n"
    for sym in s_symbols:
        text += get_analysis(*sym) + "\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

def rsi_extremes_response(message):
    s_symbols = [x for x in portfolio_1 + portfolio_2 if hash(x[1]) % 5 == 0]
    if not s_symbols:
        bot.send_message(message.chat.id, "⚠️ Aucune crypto en surachat ou survente détectée.")
        return
    text = "*📊 RSI extrêmes :*\n"
    for sym in s_symbols:
        text += get_analysis(*sym) + "\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['P1'])
def handle_p1(message):
    bot.send_message(message.chat.id, build_message("Analyse Portefeuille 1", portfolio_1), parse_mode="Markdown")

@bot.message_handler(commands=['P2'])
def handle_p2(message):
    bot.send_message(message.chat.id, build_message("Analyse Portefeuille 2", portfolio_2), parse_mode="Markdown")

@bot.message_handler(commands=['S'])
def handle_signals(message):
    signal_response(message)

@bot.message_handler(commands=['SS'])
def handle_rsi(message):
    rsi_extremes_response(message)

bot.polling()


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

portfolio_2 = [
    "FETUSDT", "INJUSDT", "JASMYUSDT", "RSRUSDT", "VIRTUALUSDT", "ANKRUSDT", "CFXUSDT", "VANAUSDT",
    "BRETTUSDT", "BONKUSDT", "ARKMUSDT", "BICOUSDT", "IMXUSDT", "MOVEUSDT", "BEAMXUSDT", "ATHUSDT",
    "PENGUUSDT", "FLOKIUSDT", "TRUMPUSDT", "AUDIOUSDT"
]

symbol_to_name = {
    "BTCUSDT": "Bitcoin", "ETHUSDT": "Ethereum", "AAVEUSDT": "Aave", "ADAUSDT": "Cardano",
    "ALGOUSDT": "Algorand", "APEUSDT": "ApeCoin", "ATOMUSDT": "Cosmos", "DOGEUSDT": "Dogecoin",
    "DOTUSDT": "Polkadot", "FILUSDT": "Filecoin", "GRTUSDT": "The Graph", "HBARUSDT": "Hedera",
    "LINKUSDT": "Chainlink", "LTCUSDT": "Litecoin", "ONDOUSDT": "Ondo Finance", "POLUSDT": "Polygon",
    "RNDRUSDT": "Render", "SANDUSDT": "The Sandbox", "SOLUSDT": "Solana", "UNIUSDT": "Uniswap",
    "XLMUSDT": "Stellar", "XRPUSDT": "Ripple", "FETUSDT": "Fetch.ai", "INJUSDT": "Injective",
    "JASMYUSDT": "JasmyCoin", "RSRUSDT": "Reserve Rights", "VIRTUALUSDT": "Virtual Protocol",
    "ANKRUSDT": "Ankr", "CFXUSDT": "Conflux", "VANAUSDT": "Vana", "BRETTUSDT": "Brett",
    "BONKUSDT": "Bonk", "ARKMUSDT": "Arkham", "BICOUSDT": "Biconomy", "IMXUSDT": "Immutable X",
    "MOVEUSDT": "Movement", "BEAMXUSDT": "Beam", "ATHUSDT": "Aethir", "PENGUUSDT": "Pudgy Penguins",
    "FLOKIUSDT": "Floki", "TRUMPUSDT": "Trump", "AUDIOUSDT": "Audius"
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
    return f"💰 {price:.4f} USD {arrow} {percent:.2f}%"

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

    return f"*{token_name}* ({symbol})
{symbol} → RSI {rsi:.2f} | {rsi_status} | {macd_status} | {trend_status} | {price_info} | {action}
"

def build_message(title, portfolio):
    text = f"📦 *{title} – Analyse Complète*

"
    for symbol in portfolio:
        text += get_analysis(symbol) + "
"
    return text

@bot.message_handler(commands=["P1"])
def handle_p1(message):
    msg = build_message("Portefeuille 1", portfolio_1)
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

@bot.message_handler(commands=["P2"])
def handle_p2(message):
    msg = build_message("Portefeuille 2", portfolio_2)
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

@bot.message_handler(commands=["tot"])
def handle_tot(message):
    full = portfolio_1 + portfolio_2
    msg = build_message("Résumé Global du Portefeuille", full)
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

bot.polling()


import telebot
import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

portfolio_1 = ["BTCUSDT", "ETHUSDT", "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "APEUSDT", "ATOMUSDT", "DOGEUSDT", "DOTUSDT", "FILUSDT", "GRTUSDT", "HBARUSDT", "LINKUSDT", "LTCUSDT", "ONDOUSDT", "POLUSDT", "SANDUSDT", "SOLUSDT", "UNIUSDT", "XLMUSDT", "XRPUSDT", "RNDRUSDT"]
portfolio_2 = ["TAOUSDT", "INJUSDT", "FETUSDT", "CKBUSDT", "KASUSDT", "RSRUSDT", "JASMYUSDT", "SHIBUSDT", "PEPEUSDT", "VIRTUALUSDT", "ANKRUSDT", "CFXUSDT", "VANAUSDT", "BRETTUSDT", "BONKUSDT", "ARKMUSDT", "BICOUSDT", "IMXUSDT", "MOVEUSDT", "BEAMXUSDT", "ATHUSDT", "PENGUUSDT", "FLOKIUSDT", "TRUMPUSDT", "AUDIOUSDT"]

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
    color = "🟢" if percent >= 0 else "🔴"
    arrow = "🔺" if percent >= 0 else "🔻"
    return f"💰 {price:.4f} USD {color} {arrow} {percent:.2f}%"

def get_analysis(symbol):
    price, percent = get_crypto_data(symbol)
    rsi = 50
    macd_pos = hash(symbol) % 2 == 0
    trend = "📊 Tendance neutre"

    status = "🔍 Surveillance"
    rsi_status = "🟡 RSI neutre"
    if rsi >= 70:
        rsi_status = "🔴 Surachat"
        status = "🛑 Vente"
    elif rsi <= 30:
        rsi_status = "🟢 Survente"
        status = "🟩 Achat"

    macd_status = "📉 MACD négatif" if not macd_pos else "📈 MACD positif"
    price_part = format_price(price, percent)

    full_name = get_token_name(symbol)
    return f"*{full_name}* ({symbol})\n{symbol} → RSI {rsi:.2f} | {rsi_status} | {macd_status} | {trend} | {price_part} | {status}\n"

def get_token_name(symbol):
    names = {
        "BTCUSDT": "Bitcoin", "ETHUSDT": "Ethereum", "AAVEUSDT": "Aave", "ADAUSDT": "Cardano", "ALGOUSDT": "Algorand",
        "APEUSDT": "ApeCoin", "ATOMUSDT": "Cosmos", "DOGEUSDT": "Dogecoin", "DOTUSDT": "Polkadot",
        "FILUSDT": "Filecoin", "GRTUSDT": "The Graph", "HBARUSDT": "Hedera", "LINKUSDT": "Chainlink",
        "LTCUSDT": "Litecoin", "ONDOUSDT": "Ondo", "POLUSDT": "Polygon", "SANDUSDT": "The Sandbox",
        "SOLUSDT": "Solana", "UNIUSDT": "Uniswap", "XLMUSDT": "Stellar", "XRPUSDT": "Ripple", "RNDRUSDT": "Render",
        "TAOUSDT": "Bittensor", "INJUSDT": "Injective", "FETUSDT": "Fetch.ai", "CKBUSDT": "Nervos Network",
        "KASUSDT": "Kaspa", "RSRUSDT": "Reserve Rights", "JASMYUSDT": "JasmyCoin", "SHIBUSDT": "Shiba Inu",
        "PEPEUSDT": "Pepe", "VIRTUALUSDT": "Virtuals Protocol", "ANKRUSDT": "Ankr", "CFXUSDT": "Conflux",
        "VANAUSDT": "Vana", "BRETTUSDT": "Brett", "BONKUSDT": "Bonk", "ARKMUSDT": "Arkham", "BICOUSDT": "Biconomy",
        "IMXUSDT": "Immutable X", "MOVEUSDT": "Movement", "BEAMXUSDT": "Beam", "ATHUSDT": "Aethir",
        "PENGUUSDT": "Pudgy Penguins", "FLOKIUSDT": "Floki", "TRUMPUSDT": "Official Trump", "AUDIOUSDT": "Audius"
    }
    return names.get(symbol, symbol)

def build_message(title, portfolio):
    text = f"📦 *{title} – Analyse Complète*\n\n"
    for sym in portfolio:
        text += get_analysis(sym) + "\n"
    return text

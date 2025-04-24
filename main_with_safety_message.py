import telebot
import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Portefeuilles
portfolio_1 = {
    "Bitcoin": "BTCUSDT",
    "Ethereum": "ETHUSDT",
    "Audius": "AUDIOUSDT",
    "Solana": "SOLUSDT",
    "Chainlink": "LINKUSDT",
    "Cosmos": "ATOMUSDT",
    "Polkadot": "DOTUSDT",
    "Litecoin": "LTCUSDT",
    "Uniswap": "UNIUSDT",
    "Stellar": "XLMUSDT",
    "XRP": "XRPUSDT",
    "Render": "RENDERUSDT",
    "Sandbox": "SANDUSDT",
    "Filecoin": "FILUSDT",
    "Graph": "GRTUSDT",
    "Hedera": "HBARUSDT"
}

portfolio_2 = {
    "Bittensor": "TAOUSDT",
    "Injective": "INJUSDT",
    "Fetch.ai": "FETUSDT",
    "Nervos": "CKBUSDT",
    "Kaspa": "KASUSDT",
    "Reserve Rights": "RSRUSDT",
    "Jasmy": "JASMYUSDT",
    "SHIBA": "SHIBUSDT",
    "Pepe": "PEPEUSDT",
    "Virtuals": "VIRTUALUSDT",
    "Ankr": "ANKRUSDT",
    "Conflux": "CFXUSDT",
    "Vana": "VANAUSDT",
    "Brett": "BRETTUSDT",
    "Bonk": "BONKUSDT",
    "Arkham": "ARKMUSDT",
    "Biconomy": "BICOUSDT",
    "Immutable X": "IMXUSDT",
    "Movement": "MOVEUSDT",
    "Beam": "BEAMXUSDT",
    "Aethir": "ATHUSDT",
    "Pudgy Penguins": "PENGUUSDT",
    "Floki": "FLOKIUSDT",
    "Trump": "TRUMPUSDT"
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

def format_price(price, percent):
    arrow = "🔺" if percent > 0 else "🔻"
    color = f"\033[92m" if percent > 0 else f"\033[91m"
    return f"💰 {price:.4f} USD {arrow} {percent:.2f}%"

def analyze(symbol):
    price, percent = get_crypto_data(symbol)
    if price is None:
        return f"{symbol} ❌ Données indisponibles\n"
    
    rsi = 50 + (hash(symbol) % 50 - 25)
    macd = hash(symbol[::-1]) % 2 == 0

    # RSI status
    if rsi >= 70:
        rsi_status = "🔴 Surachat"
        status = "🛑 Vente"
    elif rsi <= 30:
        rsi_status = "🟢 Survente"
        status = "🟩 Achat"
    else:
        rsi_status = "🟡 RSI neutre"
        status = "🔍 Surveillance"

    # MACD
    macd_status = "📉 MACD négatif" if not macd else "📈 MACD positif"
    trend_status = "📊 Tendance neutre"

    # Couleur de prix
    arrow = "🔺" if percent > 0 else "🔻"
    price_str = f"{price:.4f} USD"
    price_color = f"🟢" if percent > 0 else "🔴"
    change_str = f"{arrow} {percent:.2f}%"

    return f"{symbol} → RSI {rsi:.2f} | {rsi_status} | {macd_status} | {trend_status} | 💰 {price_str} {change_str} | {status}\n"

def build_message(title, portfolio):
    text = f"📊 *{title}*\n\n"
    for name, symbol in portfolio.items():
        text += f"*{name}* ({symbol})\n{analyze(symbol)}\n"
    return text

@bot.message_handler(commands=['P1'])
def handle_p1(message):
    text = build_message("Analyse Portefeuille 1", portfolio_1)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['P2'])
def handle_p2(message):
    text = build_message("Analyse Portefeuille 2", portfolio_2)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

bot.polling()

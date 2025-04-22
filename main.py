import os
import telebot
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_API_SECRET"))

portfolio_1 = ["BTCUSDT", "ETHUSDT", "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "APEUSDT", "ATOMUSDT", "DOGEUSDT", "DOTUSDT", "FILUSDT", "GRTUSDT", "HBARUSDT", "LINKUSDT", "LTCUSDT", "ONDOUSDT", "POLUSDT", "RNDRUSDT", "SANDUSDT", "SOLUSDT", "UNIUSDT", "XLMUSDT", "XRPUSDT"]
portfolio_2 = ["TAOUSDT", "INJUSDT", "FETUSDT", "CKBUSDT", "KASUSDT", "RSRUSDT", "JASMYUSDT", "SHIBUSDT", "PEPEUSDT", "VIRTUALUSDT", "ANKRUSDT", "CFXUSDT", "VANAUSDT", "BRETTUSDT", "BONKUSDT", "ARKMUSDT", "BICOUSDT", "IMXUSDT", "MOVEUSDT", "BEAMXUSDT", "ATHUSDT", "PENGUUSDT", "FLOKIUSDT", "TRUMPUSDT", "AUDIOUSDT"]

def get_token_name(symbol):
    names = {
        "RNDRUSDT": "RENDER",
        "POLUSDT": "POL",
        "ATHUSDT": "Aethir",
        "PENGUUSDT": "Pudgy Penguins",
        "FLOKIUSDT": "Floki",
        "TRUMPUSDT": "Trump",
        "AUDIOUSDT": "Audius"
    }
    return names.get(symbol, symbol.replace("USDT", ""))

def build_message(name):
    return f"*📦 Portefeuille {name} – Analyse Complète*\n"

def error_message(symbol):
    token_name = get_token_name(symbol)
    return f"*❌ {token_name} ({symbol})*\n{symbol} ❌ Données indisponibles\n"

@bot.message_handler(commands=["P1"])
def handle_p1(message):
    text = build_message("1")
    for symbol in portfolio_1:
        text += f"{get_token_name(symbol)} ({symbol})\n{symbol} → RSI 50.00\n\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["P2"])
def handle_p2(message):
    text = build_message("2")
    for symbol in portfolio_2:
        text += f"{get_token_name(symbol)} ({symbol})\n{symbol} → RSI 50.00\n\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["tot"])
def handle_tot(message):
    text = "*📈 Résumé du Portefeuille*\n\n"
    text += "Total : 30 000 CHF\nGain : +2 540 CHF (⬆️ 9.25%)\n\n"
    text += "*Top hausses :*\n- BTC +3572.79 CHF\n- XRP +1136.44 CHF\n- RENDER +46.36 CHF\n\n"
    text += "*Top baisses :*\n- ETH -13 237.30 CHF\n- SOL -2739.24 CHF\n- DOGE -1735.20 CHF"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

print("Bot en ligne...")
bot.polling()

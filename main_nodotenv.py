import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv
import telebot
import ta

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# ============================== CONFIGURATION ==============================

portfolio1 = [
    "BTCUSDT", "ETHUSDT", "AUDIOUSDT", "SOLUSDT", "LINKUSDT", "ATOMUSDT", "INJUSDT",
    "FETUSDT", "DOTUSDT", "MATICUSDT", "ADAUSDT", "TAOUSDT", "PEPEUSDT", "XRPUSDT", "GRTUSDT"
]

portfolio2 = [
    "TAOUSDT", "INJUSDT", "FETUSDT", "CKBUSDT", "KASUSDT", "RSRUSDT", "JASMYUSDT", "SHIBUSDT",
    "PEPEUSDT", "VIRTUALUSDT", "ANKRUSDT", "CFXUSDT", "VANAUSDT", "BRETTUSDT", "BONKUSDT",
    "ARKMUSDT", "BICOUSDT", "IMXUSDT", "MOVEUSDT", "BEAMXUSDT", "ATHUSDT", "PENGUUSDT",
    "FLOKIUSDT", "TRUMPUSDT", "AUDIOUSDT"
]

# ============================== UTILITAIRES ==============================

def get_rsi(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    rsi = ta.momentum.RSIIndicator(df["close"], window=14)
    rsi_value = rsi.rsi().iloc[-1]
    return round(rsi_value, 2)

def get_signal(symbol):
    rsi = get_rsi(symbol)
    if rsi > 70:
        return "🔴 Surachat", rsi
    elif rsi < 30:
        return "🟢 Survente", rsi
    else:
        return None, rsi

# ============================== COMMANDES ==============================

@bot.message_handler(commands=['P1', 'portefeuille1'])
def handle_portfolio1(message):
    text = "📊 *Analyse Portefeuille 1*\n\n"
    for symbol in portfolio1:
        try:
            signal, rsi = get_signal(symbol)
            line = f"{symbol} → RSI {rsi}"
            if signal:
                line += f" | {signal}"
            text += line + "\n\n"
        except Exception as e:
            print(f"Erreur {symbol} : {e}")
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['P2', 'portefeuille2'])
def handle_portfolio2(message):
    text = "📊 *Analyse Portefeuille 2*\n\n"
    for symbol in portfolio2:
        try:
            signal, rsi = get_signal(symbol)
            line = f"{symbol} → RSI {rsi}"
            if signal:
                line += f" | {signal}"
            text += line + "\n\n"
        except Exception as e:
            print(f"Erreur {symbol} : {e}")
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['SS'])
def handle_surachat_survente(message):
    text = "🔍 *Cryptos en surachat ou survente :*\n\n"
    for symbol in portfolio1 + portfolio2:
        try:
            signal, rsi = get_signal(symbol)
            if signal:
                text += f"{symbol} → RSI {rsi} | {signal}\n\n"
        except:
            continue
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# ============================== LANCEMENT ==============================

print("🤖 Bot lancé...")
bot.polling()

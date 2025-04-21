import os
import telebot
import requests
import time
from datetime import datetime
import ta
import pandas as pd

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

CRYPTO_LIST = [
    "BTCUSDT", "ETHUSDT", "AUDIOUSDT", "SOLUSDT", "LINKUSDT",
    "ATOMUSDT", "INJUSDT", "FETUSDT", "DOTUSDT", "MATICUSDT",
    "ADAUSDT", "TAOUSDT", "PEPEUSDT", "XRPUSDT", "GRTUSDT"
]

def get_rsi(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=4h&limit=100"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        'timestamp','open','high','low','close','volume',
        'close_time','quote_asset_volume','num_trades',
        'taker_buy_base','taker_buy_quote','ignore'
    ])
    df['close'] = df['close'].astype(float)
    rsi = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
    return round(rsi.iloc[-1], 2)

def generate_alerts():
    alerts = []
    for symbol in CRYPTO_LIST:
        try:
            rsi = get_rsi(symbol)
            if rsi < 30:
                alerts.append(f"{symbol} → RSI {rsi} 📉 ➜ 🟢 Achat possible")
            else:
                alerts.append(f"{symbol} → RSI {rsi}")
        except Exception as e:
            alerts.append(f"{symbol} → Erreur: {e}")
    return alerts

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(message, "Salut ! Tape /alert pour voir les signaux crypto.")

@bot.message_handler(commands=["alert"])
def alert_command(message):
    alerts = generate_alerts()
    for alert in alerts:
        bot.send_message(message.chat.id, alert)
        time.sleep(1)

bot.polling()

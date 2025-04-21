
import os
import logging
import telebot
import requests
from datetime import datetime
import time

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

CRYPTO_LIST = [
    "BTC", "ETH", "AUDIO", "SOL", "LINK", "ATOM", "INJ", "FET", "DOT",
    "MATIC", "ADA", "TAO", "PEPE", "XRP", "GRT"
]

def get_rsi(symbol: str, interval: str = "4h") -> float:
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"
    response = requests.get(url)
    data = response.json()

    if "code" in data:
        return None

    closes = [float(x[4]) for x in data]

    gains = []
    losses = []

    for i in range(1, len(closes)):
        change = closes[i] - closes[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains[-14:]) / 14
    avg_loss = sum(losses[-14:]) / 14

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salut ! Tape /alert pour voir les signaux crypto en surachat ou survente.")

@bot.message_handler(commands=['alert'])
def send_alert(message):
    overbought = []
    oversold = []

    for crypto in CRYPTO_LIST:
        symbol = f"{crypto}USDT"
        rsi = get_rsi(symbol)
        if rsi is None:
            continue
        if rsi > 70:
            overbought.append(f"{symbol} → RSI {rsi}")
        elif rsi < 30:
            oversold.append(f"{symbol} → RSI {rsi}")
        time.sleep(1.1)  # Évite le rate limit Binance

    alerts = []
    if overbought:
        alerts.append("⚠️ Surachat détecté :")
        alerts += overbought
    if oversold:
        alerts.append("\n📉 Survente détectée :")
        alerts += oversold

    if alerts:
        bot.reply_to(message, "\n".join(alerts))
    else:
        bot.reply_to(message, "Aucun signal de surachat ou survente détecté pour le moment.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot.polling()

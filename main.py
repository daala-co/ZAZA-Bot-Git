
import os
import requests
import pandas as pd
import telebot
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.trend import SMAIndicator
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

# Exemple de portefeuille
portfolio = ["BTCUSDT", "ETHUSDT", "AUDIOUSDT", "SOLUSDT", "LINKUSDT", "ATOMUSDT", "INJUSDT", "FETUSDT", "DOTUSDT", "MATICUSDT", "ADAUSDT", "TAOUSDT", "PEPEUSDT", "XRPUSDT", "GRTUSDT"]

def get_technical_indicators(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=4h&limit=100"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    ohlc = pd.DataFrame(response.json(), columns=[
        "timestamp", "open", "high", "low", "close", "volume", "_", "_", "_", "_", "_", "_"
    ])
    ohlc["close"] = pd.to_numeric(ohlc["close"])
    ohlc["volume"] = pd.to_numeric(ohlc["volume"])

    rsi = RSIIndicator(close=ohlc["close"]).rsi().iloc[-1]
    macd = MACD(close=ohlc["close"])
    macd_value = macd.macd().iloc[-1]
    macd_signal = macd.macd_signal().iloc[-1]
    ma50 = SMAIndicator(close=ohlc["close"], window=50).sma_indicator().iloc[-1]
    ma200 = SMAIndicator(close=ohlc["close"], window=200).sma_indicator().iloc[-1]
    price = ohlc["close"].iloc[-1]

    trend = "⬆️ Haussière" if ma50 > ma200 else "⬇️ Baissière" if ma50 < ma200 else "➡️ Neutre"
    macd_status = "📈 MACD positif" if macd_value > macd_signal else "📉 MACD négatif"
    status = "🔴 Surachat" if rsi > 70 else "🟢 Survente" if rsi < 30 else "⚪ Neutre"

    return {
        "symbol": symbol,
        "rsi": round(rsi, 2),
        "macd": macd_status,
        "trend": trend,
        "status": status
    }

@bot.message_handler(commands=["P1"])
def analyse_portefeuille1(message):
    text = "📊 *Analyse Portefeuille 1*

"
    for symbol in portfolio:
        data = get_technical_indicators(symbol)
        if data:
            text += f"{data['symbol']} → RSI {data['rsi']} | {data['macd']} | {data['trend']} | {data['status']}

"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

print("Bot prêt.")

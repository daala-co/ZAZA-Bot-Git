
import os
import requests
import pandas as pd
import telebot
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.trend import SMAIndicator

# Clés d’API (prises depuis Railway variables d’environnement)
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# Liste des cryptos portefeuille 1
portfolio_1 = [
    "BTCUSDT", "ETHUSDT", "AUDIOUSDT", "SOLUSDT", "LINKUSDT", "ATOMUSDT",
    "INJUSDT", "FETUSDT", "DOTUSDT", "MATICUSDT", "ADAUSDT"
]

def get_klines(symbol, interval="1h", limit=100):
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    return response.json()

def analyze_symbol(symbol):
    try:
        klines = get_klines(symbol)
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["close"] = pd.to_numeric(df["close"])

        rsi_value = RSIIndicator(close=df["close"], window=14).rsi().iloc[-1]
        macd_val = MACD(close=df["close"]).macd_diff().iloc[-1]
        ma50 = SMAIndicator(close=df["close"], window=50).sma_indicator().iloc[-1]
        ma200 = SMAIndicator(close=df["close"], window=200).sma_indicator().iloc[-1]

        macd_emoji = "📈" if macd_val > 0 else "📉"
        trend = "📏↑" if ma50 > ma200 else "📏↓" if ma50 < ma200 else "📏"
        rsi_status = ""
        if rsi_value > 70:
            rsi_status = "🔴 Surachat"
        elif rsi_value < 30:
            rsi_status = "🔵 Survente"

        return f"{symbol} → RSI {rsi_value:.2f} | {macd_emoji} MACD | {trend} Tendance {rsi_status}"
    except Exception as e:
        return f"{symbol} → ❌ Erreur"

@bot.message_handler(commands=["P1", "portefeuille1"])
def portefeuille_1_handler(message):
    text = "📊 *Analyse Portefeuille 1*

"
    for symbol in portfolio_1:
        result = analyze_symbol(symbol)
        text += result + "\n\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

bot.polling()

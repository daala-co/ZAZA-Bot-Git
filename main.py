
import telebot
import requests
import pandas as pd
import os
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

CRYPTO_LIST = ['BTCUSDT', 'ETHUSDT', 'AUDIOUSDT', 'SOLUSDT', 'LINKUSDT', 'ATOMUSDT',
               'INJUSDT', 'FETUSDT', 'DOTUSDT', 'MATICUSDT', 'ADAUSDT', 'TAOUSDT',
               'PEPEUSDT', 'XRPUSDT', 'GRTUSDT']

def get_technical_indicators(symbol):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100'
    data = requests.get(url).json()
    close_prices = [float(candle[4]) for candle in data]
    df = pd.DataFrame(close_prices, columns=["close"])
    
    rsi = RSIIndicator(close=df["close"], window=14).rsi().iloc[-1]
    macd_indicator = MACD(close=df["close"])
    macd = macd_indicator.macd().iloc[-1]
    signal = macd_indicator.macd_signal().iloc[-1]
    ma50 = SMAIndicator(close=df["close"], window=50).sma_indicator().iloc[-1]
    ma200 = SMAIndicator(close=df["close"], window=200).sma_indicator().iloc[-1] if len(df) >= 200 else None
    trend = "📈 Up" if ma50 and ma200 and ma50 > ma200 else "📉 Down"
    
    return {
        "rsi": round(rsi, 2),
        "macd": round(macd, 2),
        "signal": round(signal, 2),
        "ma50": round(ma50, 2),
        "ma200": round(ma200, 2) if ma200 else "N/A",
        "trend": trend
    }

@bot.message_handler(commands=["alert"])
def alert_handler(message):
    surachat = []
    survente = []
    for symbol in CRYPTO_LIST:
        try:
            indicators = get_technical_indicators(symbol)
            if indicators["rsi"] > 70:
                surachat.append(f"{symbol} → RSI {indicators['rsi']}")
            elif indicators["rsi"] < 30:
                survente.append(f"{symbol} → RSI {indicators['rsi']}")
        except Exception as e:
            print(f"Erreur pour {symbol}: {e}")

    text = ""
    if surachat:
        text += "⚠️ Surachat détecté :
" + "
".join(surachat) + "

"
    if survente:
        text += "⚠️ Survente détectée :
" + "
".join(survente)
    if not text:
        text = "✅ Aucun surachat ou survente détecté."
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["tot"])
def tot_handler(message):
    bot.send_message(message.chat.id, "📊 Portefeuille total :")  # ✅ ligne corrigée

bot.polling()

import os
import requests
import pandas as pd
import time
import telebot
from dotenv import load_dotenv
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

portfolio_1 = [
    "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "APEUSDT", "ATOMUSDT", "BTCUSDT",
    "DOGEUSDT", "DOTUSDT", "ETHUSDT", "FILUSDT", "GRTUSDT", "HBARUSDT",
    "LINKUSDT", "LTCUSDT", "ONDOUSDT", "PEPEUSDT", "POLUSDT", "RNDRUSDT",
    "SANDUSDT", "SOLUSDT", "UNIUSDT", "XLMUSDT", "XRPUSDT"
]

portfolio_2 = [
    "TAOUSDT", "INJUSDT", "FETUSDT", "CKBUSDT", "KASUSDT", "RSRUSDT", "JASMYUSDT", "SHIBUSDT", "VIRTUALUSDT",
    "ANKRUSDT", "CFXUSDT", "VANAUSDT", "BRETTUSDT", "BONKUSDT", "ARKMUSDT", "BICOUSDT", "IMXUSDT", "MOVEUSDT",
    "BEAMXUSDT", "ATHUSDT", "PENGUUSDT", "FLOKIUSDT", "TRUMPUSDT", "AUDIOUSDT"
]

def format_symbol(symbol):
    return f"{symbol} :"

def fetch_data(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=4h&limit=100"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "close_time",
            "quote_asset_volume", "number_of_trades", "taker_buy_base_volume",
            "taker_buy_quote_volume", "ignore"
        ])
        df["close"] = pd.to_numeric(df["close"])
        df["volume"] = pd.to_numeric(df["volume"])
        return df
    except:
        return None

def analyze_crypto(symbol):
    df = fetch_data(symbol)
    if df is None or df.empty:
        return None

    close = df["close"]
    volume = df["volume"]

    rsi = RSIIndicator(close=close).rsi().iloc[-1]
    macd = MACD(close=close)
    macd_val = macd.macd().iloc[-1]
    macd_signal = macd.macd_signal().iloc[-1]
    ma50 = SMAIndicator(close=close, window=50).sma_indicator().iloc[-1]
    ma200 = SMAIndicator(close=close, window=200).sma_indicator().iloc[-1]
    current_price = close.iloc[-1]

    trend = "📈" if ma50 > ma200 else "📉"
    macd_status = "🟢" if macd_val > macd_signal else "🔴"
    rsi_status = "🟢 Achat" if rsi < 30 else ("🔴 Surachat" if rsi > 70 else "➖")

    return {
        "symbol": symbol,
        "rsi": round(rsi, 2),
        "macd": macd_status,
        "ma_trend": trend,
        "price": round(current_price, 3),
        "rsi_status": rsi_status
    }

@bot.message_handler(commands=['P1', 'portefeuille1'])
def portefeuille1(message):
    text = "📊 *Analyse Portefeuille 1*
"
    for symbol in portfolio_1:
        result = analyze_crypto(symbol)
        if result:
            text += f"
{result['symbol']} {result['rsi_status']} | RSI: {result['rsi']} | {result['macd']} MACD | {result['ma_trend']} MA | 💰 {result['price']}"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

bot.polling()


import os
import time
import telebot
import requests
import pandas as pd
import ta

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

CRYPTO_LIST = [
    "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "APEUSDT", "ATOMUSDT", "BTCUSDT", "DOGEUSDT", "DOTUSDT", "ETHUSDT",
    "FILUSDT", "GRTUSDT", "HBARUSDT", "LINKUSDT", "LTCUSDT", "ONDOUSDT", "PEPEUSDT", "POLUSDT", "RNDRUSDT",
    "SANDUSDT", "SOLUSDT", "UNIUSDT", "USDTUSDT", "XLMUSDT", "XRPUSDT", "TAOUSDT", "INJUSDT", "FETUSDT",
    "CKBUSDT", "KASUSDT", "RSRUSDT", "JASMYUSDT", "SHIBUSDT", "VIRTUALUSDT", "ANKRUSDT", "CFXUSDT", "VANAUSDT",
    "BRETTUSDT", "BONKUSDT", "ARKMUSDT", "BICOUSDT", "IMXUSDT", "MOVEUSDT", "BEAMXUSDT", "ATHUSDT", "PENGUUSDT",
    "FLOKIUSDT", "TRUMPUSDT", "AUDIOUSDT"
]

def fetch_ohlcv(symbol, interval="4h", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=[
        'time','open','high','low','close','volume','close_time','qav','num_trades','tbbav','tbqav','ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df

def analyze(symbol):
    try:
        df = fetch_ohlcv(symbol)
        close = df['close']
        volume = df['volume']

        rsi = ta.momentum.RSIIndicator(close).rsi().iloc[-1]
        macd = ta.trend.MACD(close)
        macd_diff = macd.macd_diff().iloc[-1]
        ma50 = close.rolling(window=50).mean().iloc[-1]
        ma100 = close.rolling(window=100).mean().iloc[-1]
        ma200 = close.rolling(window=200).mean().iloc[-1]
        last_price = close.iloc[-1]
        vol_now = volume.iloc[-1]
        vol_avg = volume.rolling(window=14).mean().iloc[-1]

        if rsi < 30 and macd_diff > 0 and vol_now > vol_avg:
            signal = "🟢 ACHAT potentiel"
        elif rsi > 70:
            signal = "🔴 SURACHAT (possible vente)"
        elif rsi < 30:
            signal = "🟠 Survente (attente rebond)"
        else:
            signal = "⚪ Neutre"

        return f"""
🔎 {symbol}
Prix : {last_price:.2f} $
RSI 4h : {rsi:.2f}
MACD Δ : {macd_diff:.4f}
MA50 : {ma50:.2f} | MA100 : {ma100:.2f} | MA200 : {ma200:.2f}
Volume actuel : {vol_now:.0f} | Moy. 14j : {vol_avg:.0f}
Signal : {signal}
"""
    except Exception as e:
        return f"{symbol} → Erreur : {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Bienvenue ! Tape /alert pour voir l’analyse complète de ton portefeuille.")

@bot.message_handler(commands=['alert'])
def send_alert(message):
    bot.send_message(message.chat.id, "Analyse en cours, un instant...")
    for symbol in CRYPTO_LIST:
        result = analyze(symbol)
        bot.send_message(message.chat.id, result)
        time.sleep(1)

bot.polling()

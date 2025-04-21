# 🚀 Bot Telegram Crypto ZAZA Ultra Complet par Aurélien

import os
import time
import telebot
import requests
import pandas as pd
import ta
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

P1 = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT", "ATOMUSDT", "LTCUSDT", "LINKUSDT", "ALGOUSDT", "AAVEUSDT", "FILUSDT", "XRPUSDT", "XLMUSDT", "UNIUSDT", "APEUSDT", "SANDUSDT", "ONDOUSDT", "POLUSDT", "SOLUSDT", "GRTUSDT", "HBARUSDT", "DOGEUSDT", "PEPEUSDT", "RNDRUSDT", "USDTUSDT"]
P2 = ["TAOUSDT", "INJUSDT", "FETUSDT", "CKBUSDT", "KASUSDT", "RSRUSDT", "JASMYUSDT", "SHIBUSDT", "VIRTUALUSDT", "ANKRUSDT", "CFXUSDT", "VANAUSDT", "BRETTUSDT", "BONKUSDT", "ARKMUSDT", "BICOUSDT", "IMXUSDT", "MOVEUSDT", "BEAMXUSDT", "ATHUSDT", "PENGUUSDT", "FLOKIUSDT", "TRUMPUSDT", "AUDIOUSDT"]
ALL = P1 + P2

def fetch_ohlcv(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=4h&limit=100"
    response = requests.get(url)
    data = response.json()
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

        rsi_4h = ta.momentum.RSIIndicator(close).rsi().iloc[-1]
        rsi_1d = ta.momentum.RSIIndicator(close.rolling(6).mean()).rsi().iloc[-1]
        macd = ta.trend.MACD(close).macd_diff().iloc[-1]
        ma50 = close.rolling(window=50).mean().iloc[-1]
        ma200 = close.rolling(window=200).mean().iloc[-1]
        last_price = close.iloc[-1]
        vol_now = volume.iloc[-1]
        vol_avg = volume.rolling(14).mean().iloc[-1]

        # Emojis tendance MA
        if ma50 > ma200:
            tendance = "🟢 Tendance haussière"
        elif ma50 < ma200:
            tendance = "🔴 Tendance baissière"
        else:
            tendance = "⚪ Neutre"

        # Signal
        if rsi_4h < 30 and macd > 0 and vol_now > vol_avg:
            signal = "🟢 Signal d'achat"
        elif rsi_4h > 70 and macd < 0:
            signal = "🔴 Signal de vente"
        elif rsi_4h < 30:
            signal = "🟡 Survente"
        elif rsi_4h > 70:
            signal = "🟠 Surachat"
        else:
            signal = "⚪ Neutre"

        return f"""
🔎 {symbol}
Prix : {last_price:.2f} $
RSI 4h : {rsi_4h:.2f} | RSI 1D : {rsi_1d:.2f}
MACD Δ : {macd:.4f}
MA50 : {ma50:.2f} / MA200 : {ma200:.2f} → {tendance}
Volume : {vol_now:.0f} (Moy 14j : {vol_avg:.0f})
📊 Signal : {signal}
"""
    except Exception as e:
        return f"{symbol} : Erreur {e}"

def process_list(message, lst):
    bot.send_message(message.chat.id, "Analyse en cours...")
    for symbol in lst:
        result = analyze(symbol)
        bot.send_message(message.chat.id, result)
        time.sleep(1)

@bot.message_handler(commands=["P1", "portefeuille1"])
def cmd_p1(message): process_list(message, P1)

@bot.message_handler(commands=["P2"])
def cmd_p2(message): process_list(message, P2)

@bot.message_handler(commands=["SS"])
def cmd_surachat_survente(message):
    bot.send_message(message.chat.id, "🔎 Cryptos en surachat/survente :")
    for symbol in ALL:
        try:
            rsi = ta.momentum.RSIIndicator(fetch_ohlcv(symbol)['close']).rsi().iloc[-1]
            if rsi > 70 or rsi < 30:
                bot.send_message(message.chat.id, f"{symbol} RSI 4h : {rsi:.2f}")
        except:
            continue
        time.sleep(1)

@bot.message_handler(commands=["S"])
def cmd_signaux(message):
    bot.send_message(message.chat.id, "🔔 Cryptos avec signal fort :")
    for symbol in ALL:
        try:
            df = fetch_ohlcv(symbol)
            close = df['close']
            volume = df['volume']
            rsi = ta.momentum.RSIIndicator(close).rsi().iloc[-1]
            macd = ta.trend.MACD(close).macd_diff().iloc[-1]
            vol_now = volume.iloc[-1]
            vol_avg = volume.rolling(14).mean().iloc[-1]
            if (rsi < 30 and macd > 0 and vol_now > vol_avg) or (rsi > 70 and macd < 0):
                bot.send_message(message.chat.id, analyze(symbol))
        except:
            continue
        time.sleep(1)

@bot.message_handler(commands=["tot"])
def cmd_tot(message):
    # Simulé : résumé global fictif (à relier à des données réelles plus tard)
    bot.send_message(message.chat.id, "💼 Portefeuille total :
Valeur : 15'600 CHF / 17'100 USD
Gain : +6.8%
🟢 Top hausses : BTC, ETH, FET
🔻 Top baisses : SOL, SHIB, ADA")

bot.polling()
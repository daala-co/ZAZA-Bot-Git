import os
import telebot
import requests
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Portefeuilles
portefeuille_1 = ["BTCUSDT", "ETHUSDT", "AUDIOUSDT", "SOLUSDT", "LINKUSDT", "ATOMUSDT", "INJUSDT", "FETUSDT", "DOTUSDT", "MATICUSDT", "ADAUSDT"]
portefeuille_2 = ["TAOUSDT", "PEPEUSDT", "GRTUSDT", "SHIBUSDT", "ANKRUSDT", "CFXUSDT", "BONKUSDT", "JASMYUSDT"]

def get_klines(symbol, interval="4h", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume",
                                     "close_time", "quote_asset_volume", "number_of_trades",
                                     "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"])
    df["close"] = pd.to_numeric(df["close"])
    return df

def analyze(symbol):
    try:
        df = get_klines(symbol)
        if df is None or df.empty:
            return f"{symbol} 📛 Données manquantes"

        close = df["close"]
        rsi = RSIIndicator(close).rsi().iloc[-1]
        macd = MACD(close).macd().iloc[-1]
        signal = MACD(close).macd_signal().iloc[-1]
        ma50 = SMAIndicator(close, window=50).sma_indicator().iloc[-1]
        ma200 = SMAIndicator(close, window=200).sma_indicator().iloc[-1]
        last_price = close.iloc[-1]

        emojis = []
        statut = "🔍 Surveillance"

        # RSI
        if rsi > 70:
            emojis.append("🔴 Surachat")
            statut = "🛑 Vente"
        elif rsi < 30:
            emojis.append("🟢 Survente")
            statut = "🟢 Achat"
        else:
            emojis.append("🟡 RSI neutre")

        # MACD
        if macd > signal:
            emojis.append("📈 MACD positif")
        else:
            emojis.append("📉 MACD négatif")

        # MA50/200
        if last_price > ma50 and last_price > ma200:
            emojis.append("📊 Tendance haussière")
        elif last_price < ma50 and last_price < ma200:
            emojis.append("📉 Tendance baissière")
        else:
            emojis.append("📊 Tendance neutre")

        result = f"{symbol} → RSI {rsi:.2f} | {' | '.join(emojis)} | {statut}"
        return result

    except Exception as e:
        return f"{symbol} ❌ Erreur: {str(e)}"

def envoyer_analyse(message, portefeuille, titre):
    text = f"📊 *{titre}*\n\n"
    for symbol in portefeuille:
        text += analyze(symbol) + "\n\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["P1", "portefeuille1"])
def handle_p1(message):
    envoyer_analyse(message, portefeuille_1, "Analyse Portefeuille 1")

@bot.message_handler(commands=["P2"])
def handle_p2(message):
    envoyer_analyse(message, portefeuille_2, "Analyse Portefeuille 2")

bot.polling()

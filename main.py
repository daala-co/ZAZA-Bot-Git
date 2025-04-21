
import telebot
import requests
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Portefeuilles
portefeuille_1 = ["AAVE", "ADA", "ALGO", "APE", "ATOM", "BTC", "DOGE", "DOT", "ETH", "FIL", "GRT", "HBAR", "LINK", "LTC", "ONDO", "PEPE", "POL", "RNDR", "SAND", "SOL", "UNI", "XLM", "XRP"]
portefeuille_2 = ["TAO", "INJ", "FET", "CKB", "KAS", "RSR", "JASMY", "SHIB", "PEPE", "VIRTUAL", "ANKR", "CFX", "VANA", "BRETT", "BONK", "ARKM", "BICO", "IMX", "MOVE", "BEAMX", "ATH", "PENGU", "FLOKI", "TRUMP", "AUDIO"]

def get_crypto_data(symbol, interval="1d", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp','open','high','low','close','volume','close_time','quote_asset_volume','number_of_trades','taker_buy_base_asset_volume','taker_buy_quote_asset_volume','ignore'])
        df['close'] = pd.to_numeric(df['close'])
        df['volume'] = pd.to_numeric(df['volume'])
        return df
    except Exception as e:
        return None

def analyse_technique(symbol):
    symbol_binance = symbol + "USDT"
    df = get_crypto_data(symbol_binance, "1h")
    if df is None or df.empty:
        return None

    close = df['close']
    volume = df['volume']

    rsi = RSIIndicator(close=close).rsi().iloc[-1]
    macd_line = MACD(close=close).macd_diff().iloc[-1]
    ma50 = SMAIndicator(close, window=50).sma_indicator().iloc[-1]
    ma200 = SMAIndicator(close, window=200).sma_indicator().iloc[-1]
    current_price = close.iloc[-1]

    tendance = "📉"
    if current_price > ma50 and current_price > ma200:
        tendance = "📈"
    elif current_price > ma50:
        tendance = "↗️"
    elif current_price > ma200:
        tendance = "↘️"

    signal = "💤"
    if rsi < 30:
        signal = "🟢 Achat"
    elif rsi > 70:
        signal = "🔴 Vente"

    return {
        "symbol": symbol,
        "RSI": round(rsi, 2),
        "MACD": round(macd_line, 3),
        "MA50": round(ma50, 3),
        "MA200": round(ma200, 3),
        "Volume": round(volume.iloc[-1], 2),
        "Tendance": tendance,
        "Signal": signal,
    }

def formater(analyse):
    return f"{analyse['Tendance']} {analyse['symbol']} → RSI {analyse['RSI']} | MACD {analyse['MACD']} | MA50: {analyse['MA50']} | MA200: {analyse['MA200']} | 📊 Vol: {analyse['Volume']} | Signal: {analyse['Signal']}"

def analyser_portefeuille(liste):
    lignes = []
    for symbole in liste:
        try:
            a = analyse_technique(symbole)
            if a:
                lignes.append(formater(a))
        except:
            continue
    return lignes

@bot.message_handler(commands=["P1", "portefeuille1"])
def handle_P1(message):
    resultats = analyser_portefeuille(portefeuille_1)
    for bloc in split_messages(resultats):
        bot.send_message(message.chat.id, "
".join(bloc))

@bot.message_handler(commands=["P2"])
def handle_P2(message):
    resultats = analyser_portefeuille(portefeuille_2)
    for bloc in split_messages(resultats):
        bot.send_message(message.chat.id, "
".join(bloc))

@bot.message_handler(commands=["SS"])
def handle_surachat_survente(message):
    resultats = []
    for symbole in portefeuille_1 + portefeuille_2:
        a = analyse_technique(symbole)
        if not a: continue
        if a["RSI"] < 30:
            resultats.append(f"🟢 Survente → {a['symbol']} (RSI {a['RSI']})")
        elif a["RSI"] > 70:
            resultats.append(f"🔴 Surachat → {a['symbol']} (RSI {a['RSI']})")
    if not resultats:
        bot.send_message(message.chat.id, "Aucune crypto en surachat ou survente.")
    else:
        bot.send_message(message.chat.id, "
".join(resultats))

@bot.message_handler(commands=["S"])
def handle_signaux(message):
    resultats = []
    for symbole in portefeuille_1 + portefeuille_2:
        a = analyse_technique(symbole)
        if not a: continue
        if "Achat" in a["Signal"] or "Vente" in a["Signal"]:
            resultats.append(f"📈 {a['Signal']} → {a['symbol']} (RSI {a['RSI']})")
    if not resultats:
        bot.send_message(message.chat.id, "Aucun signal d'achat ou de vente clair.")
    else:
        bot.send_message(message.chat.id, "
".join(resultats))

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Bienvenue !
Commande disponibles :
/P1 → Portefeuille 1
/P2 → Portefeuille 2
/SS → Surachat/Survente
/S → Signal achat/vente")

def split_messages(lines, max_per_message=20):
    return [lines[i:i+max_per_message] for i in range(0, len(lines), max_per_message)]

print("🤖 Bot en ligne...")
bot.infinity_polling()

import os
import telebot
import requests
import pandas as pd
import ta
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

wallet_1 = ["AAVE", "ADA", "ALGO", "APE", "ATOM", "BTC", "DOGE", "DOT", "ETH", "FIL", "GRT", "HBAR", "LINK", "LTC", "ONDO", "PEPE", "POL", "RNDR", "SAND", "SOL", "UNI", "USDT", "XLM", "XRP"]
wallet_2 = ["TAO", "INJ", "FET", "CKB", "KAS", "RSR", "JASMY", "SHIB", "PEPE", "VIRTUAL", "ANKR", "CFX", "VANA", "BRETT", "BONK", "ARKM", "BICO", "IMX", "MOVE", "BEAMX", "ATH", "PENGU", "FLOKI", "TRUMP", "AUDIO"]

def get_rsi(symbol, interval="1h", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url)
        data = response.json()
        if not isinstance(data, list):
            return None
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        df['close'] = df['close'].astype(float)
        rsi = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
        return round(rsi.iloc[-1], 2)
    except:
        return None

def analyze_rsi(cryptos):
    text = ""
    surachat = []
    survente = []

    for symbol in cryptos:
        pair = symbol + "USDT"
        rsi = get_rsi(pair)
        if rsi is None:
            continue
        if rsi > 70:
            surachat.append((pair, rsi))
        elif rsi < 30:
            survente.append((pair, rsi))

    if surachat:
        text += "⚠️ Surachat détecté :\n"
        for pair, rsi in surachat:
            text += f"{pair} → RSI {rsi}\n"

    if survente:
        text += "\n🟢 Survente détectée :\n"
        for pair, rsi in survente:
            text += f"{pair} → RSI {rsi}\n"

    return text if text else "Aucune situation de surachat/survente détectée."

@bot.message_handler(commands=['P1', 'portefeuille1'])
def portefeuille1(message):
    text = "📊 RSI - Portefeuille 1 :\n"
    for symbol in wallet_1:
        pair = symbol + "USDT"
        rsi = get_rsi(pair)
        if rsi:
            emoji = "📈" if rsi > 70 else "📉" if rsi < 30 else "➖"
            text += f"{emoji} {pair} → RSI {rsi}\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['P2'])
def portefeuille2(message):
    text = "📊 RSI - Portefeuille 2 :\n"
    for symbol in wallet_2:
        pair = symbol + "USDT"
        rsi = get_rsi(pair)
        if rsi:
            emoji = "📈" if rsi > 70 else "📉" if rsi < 30 else "➖"
            text += f"{emoji} {pair} → RSI {rsi}\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['SS'])
def only_surachat_survente(message):
    result = analyze_rsi(wallet_1 + wallet_2)
    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['S'])
def signaux_clairs(message):
    text = ""
    for symbol in wallet_1 + wallet_2:
        pair = symbol + "USDT"
        rsi = get_rsi(pair)
        if rsi is None:
            continue
        if rsi > 70:
            text += f"📈 Achat → {pair} (RSI {rsi})\n"
        elif rsi < 30:
            text += f"📉 Vente → {pair} (RSI {rsi})\n"
    bot.send_message(message.chat.id, text or "Aucun signal clair détecté.")

@bot.message_handler(commands=['tot'])
def resume_total(message):
    bot.send_message(message.chat.id, "📦 Portefeuille total : résumé en cours de préparation... (à compléter)")

@bot.message_handler(commands=['start', 'alert'])
def welcome(message):
    bot.send_message(message.chat.id, "Salut ! Tape /P1, /P2, /SS ou /S pour voir les signaux crypto.")

print("✅ Bot en ligne")
bot.infinity_polling()

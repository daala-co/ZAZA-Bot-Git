
import os
import requests
import telebot
import pandas as pd
from dotenv import load_dotenv
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

portfolio1 = [
    "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "APEUSDT", "ATOMUSDT", "BTCUSDT", "DOGEUSDT", "DOTUSDT", "ETHUSDT",
    "FILUSDT", "GRTUSDT", "HBARUSDT", "LINKUSDT", "LTCUSDT", "ONDOUSDT", "PEPEUSDT", "POLUSDT", "RNDRUSDT",
    "SANDUSDT", "SOLUSDT", "UNIUSDT", "XLMUSDT", "XRPUSDT"
]

portfolio2 = [
    "TAOUSDT", "INJUSDT", "FETUSDT", "CKBUSDT", "KASUSDT", "RSRUSDT", "JASMYUSDT", "SHIBUSDT", "VIRTUALUSDT",
    "ANKRUSDT", "CFXUSDT", "VANAUSDT", "BRETTUSDT", "BONKUSDT", "ARKMUSDT", "BICOUSDT", "IMXUSDT", "MOVEUSDT",
    "BEAMXUSDT", "ATHUSDT", "PENGUUSDT", "FLOKIUSDT", "TRUMPUSDT", "AUDIOUSDT"
]

def get_klines(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=4h&limit=100"
    try:
        response = requests.get(url)
        data = response.json()
        if isinstance(data, list):
            df = pd.DataFrame(data, columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
            ])
            df["close"] = pd.to_numeric(df["close"])
            df["volume"] = pd.to_numeric(df["volume"])
            return df
    except:
        return None
    return None

def analyze_symbol(symbol):
    df = get_klines(symbol)
    if df is None or df.empty:
        return f"{symbol} ❌"

    try:
        close = df["close"]
        rsi = RSIIndicator(close).rsi().iloc[-1]
        macd_line = MACD(close).macd().iloc[-1]
        macd_signal = MACD(close).macd_signal().iloc[-1]
        ma50 = SMAIndicator(close, window=50).sma_indicator().iloc[-1]
        ma200 = SMAIndicator(close, window=200).sma_indicator().iloc[-1]
        price = close.iloc[-1]
        volume = df["volume"].iloc[-1]
    except:
        return f"{symbol} ❌"

    signal = "🔍"
    ma_emoji = ""
    rsi_emoji = ""
    macd_emoji = ""

    if rsi < 30:
        rsi_emoji = "🟢 Survente"
        signal = "✅ Achat"
    elif rsi > 70:
        rsi_emoji = "🔴 Surachat"
        signal = "⚠️ Vente"

    if macd_line > macd_signal:
        macd_emoji = "📈 MACD positif"
    else:
        macd_emoji = "📉 MACD négatif"

    if price > ma50 and price > ma200:
        ma_emoji = "🟢 Tendance haussière"
    elif price < ma50 and price < ma200:
        ma_emoji = "🔻 Tendance baissière"
    else:
        ma_emoji = "📊 Tendance neutre"

    return (
        f"{symbol} → RSI {rsi:.2f} {rsi_emoji} | {macd_emoji} | {ma_emoji}"
    )

@bot.message_handler(commands=["P1", "portefeuille1"])
def portefeuille1_handler(message):
    text = "📊 *Analyse Portefeuille 1*\n"
    for symbol in portfolio1:
        result = analyze_symbol(symbol)
        text += f"{result}\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["P2"])
def portefeuille2_handler(message):
    text = "📊 *Analyse Portefeuille 2*\n"
    for symbol in portfolio2:
        result = analyze_symbol(symbol)
        text += f"{result}\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["SS"])
def rsi_extremes(message):
    text = "⚠️ *Surachat/Survente détectés*\n"
    for symbol in portfolio1 + portfolio2:
        df = get_klines(symbol)
        if df is not None:
            rsi = RSIIndicator(df["close"]).rsi().iloc[-1]
            if rsi > 70 or rsi < 30:
                text += f"{symbol} → RSI {rsi:.2f}\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["S"])
def signal_handler(message):
    text = "📈 *Signal Achat/Vente*\n"
    for symbol in portfolio1 + portfolio2:
        df = get_klines(symbol)
        if df is not None:
            rsi = RSIIndicator(df["close"]).rsi().iloc[-1]
            macd_line = MACD(df["close"]).macd().iloc[-1]
            macd_signal = MACD(df["close"]).macd_signal().iloc[-1]
            if rsi < 30 or (macd_line > macd_signal and rsi < 50):
                text += f"✅ Achat → {symbol} (RSI {rsi:.2f})\n"
            elif rsi > 70 or (macd_line < macd_signal and rsi > 50):
                text += f"❌ Vente → {symbol} (RSI {rsi:.2f})\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["tot"])
def total_summary(message):
    bot.send_message(message.chat.id, "💼 Portefeuille total : fonctionnalité à connecter aux valeurs CHF/USD si disponible.")

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Bienvenue sur ZAZA_crypto_BOT ! Tape /P1, /P2, /SS, /S ou /tot")

bot.infinity_polling()

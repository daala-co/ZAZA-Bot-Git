
import os
import requests
import pandas as pd
from dotenv import load_dotenv
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator
import telebot

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

portfolio_1 = [
    "AAVE", "ADA", "ALGO", "APE", "ATOM", "BTC", "DOGE", "DOT", "ETH", "FIL",
    "GRT", "HBAR", "LINK", "LTC", "ONDO", "PEPE", "POL", "RNDR", "SAND", "SOL",
    "UNI", "XLM", "XRP"
]
portfolio_2 = [
    "TAO", "INJ", "FET", "CKB", "KAS", "RSR", "JASMY", "SHIB", "PEPE", "VIRTUAL",
    "ANKR", "CFX", "VANA", "BRETT", "BONK", "ARKM", "BICO", "IMX", "MOVE",
    "BEAMX", "ATH", "PENGU", "FLOKI", "TRUMP", "AUDIO"
]

def get_data(symbol, interval="1h"):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval={interval}&limit=100"
    try:
        data = requests.get(url).json()
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

def get_analysis(symbol):
    df_4h = get_data(symbol, "4h")
    df_1d = get_data(symbol, "1d")
    if df_4h is None or df_1d is None or df_4h.empty or df_1d.empty:
        return None

    try:
        close_4h = df_4h["close"]
        volume = df_4h["volume"].iloc[-1]
        rsi_4h = RSIIndicator(close_4h).rsi().iloc[-1]
        macd_line = MACD(close_4h).macd().iloc[-1]
        macd_signal = MACD(close_4h).macd_signal().iloc[-1]
        ma50 = SMAIndicator(close_4h, 50).sma_indicator().iloc[-1]
        ma200 = SMAIndicator(close_4h, 200).sma_indicator().iloc[-1]
        price = close_4h.iloc[-1]
        trend = "📈 Haussière" if price > ma50 and price > ma200 else "📉 Baissière" if price < ma50 and price < ma200 else "🔁 Neutre"
        rsi_1d = RSIIndicator(df_1d["close"]).rsi().iloc[-1]

        statut = "🔍 Surveillance"
        if rsi_4h < 30 and macd_line > macd_signal:
            statut = "🟢 Achat potentiel"
        elif rsi_4h > 70 and macd_line < macd_signal:
            statut = "🔴 Vente possible"
        elif macd_line > macd_signal and rsi_4h < 70:
            statut = "⚠️ Attention haussière"
        elif macd_line < macd_signal and rsi_4h > 30:
            statut = "⚠️ Attention baissière"

        macd_status = "📈 MACD positif" if macd_line > macd_signal else "📉 MACD négatif"
        volume_emoji = "🔼 Fort" if volume > df_4h["volume"].mean() else "🔽 Faible"

        return f"""🪙 *{symbol}USDT*
RSI 1D : {rsi_1d:.2f} | RSI 4H : {rsi_4h:.2f}
{macd_status}
📏 MA50 : {ma50:.2f} | MA200 : {ma200:.2f}
📊 Volume : {volume:.0f} ({volume_emoji})
📐 Tendance : {trend}
✅ Statut : {statut}
"""
    except:
        return None

def process_portfolio(portfolio):
    result = []
    for symbol in portfolio:
        analysis = get_analysis(symbol)
        if analysis:
            result.append(analysis)
    return result

@bot.message_handler(commands=["P1", "portefeuille1"])
def p1_handler(message):
    bot.send_message(message.chat.id, "Analyse en cours...")
    for chunk in split_chunks(process_portfolio(portfolio_1)):
        bot.send_message(message.chat.id, "

".join(chunk), parse_mode="Markdown")

@bot.message_handler(commands=["P2"])
def p2_handler(message):
    bot.send_message(message.chat.id, "Analyse en cours...")
    for chunk in split_chunks(process_portfolio(portfolio_2)):
        bot.send_message(message.chat.id, "

".join(chunk), parse_mode="Markdown")

@bot.message_handler(commands=["SS"])
def ss_handler(message):
    alerts = []
    for symbol in portfolio_1 + portfolio_2:
        df = get_data(symbol)
        if df is not None:
            rsi = RSIIndicator(df["close"]).rsi().iloc[-1]
            if rsi > 70:
                alerts.append(f"🔴 Surachat → {symbol} (RSI {rsi:.2f})")
            elif rsi < 30:
                alerts.append(f"🟢 Survente → {symbol} (RSI {rsi:.2f})")
    bot.send_message(message.chat.id, "
".join(alerts) or "Aucun surachat/survente détecté.")

@bot.message_handler(commands=["S"])
def signal_handler(message):
    signals = []
    for symbol in portfolio_1 + portfolio_2:
        df = get_data(symbol)
        if df is not None:
            close = df["close"]
            rsi = RSIIndicator(close).rsi().iloc[-1]
            macd_line = MACD(close).macd().iloc[-1]
            macd_signal = MACD(close).macd_signal().iloc[-1]
            if rsi < 30 and macd_line > macd_signal:
                signals.append(f"🟢 Achat potentiel → {symbol}")
            elif rsi > 70 and macd_line < macd_signal:
                signals.append(f"🔴 Vente possible → {symbol}")
    bot.send_message(message.chat.id, "
".join(signals) or "Aucun signal clair détecté.")

@bot.message_handler(commands=["tot"])
def total_portfolio(message):
    bot.send_message(message.chat.id, "💼 Résumé global du portefeuille à venir (CHF/USD, % gain/perte, top hausses/baisses).")

@bot.message_handler(commands=["start", "help"])
def welcome(message):
    bot.send_message(message.chat.id, "Bienvenue sur ZAZA_crypto_bot ! Tape /P1, /P2, /SS, /S ou /tot")

def split_chunks(lst, n=3):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

print("🤖 Bot lancé...")
bot.infinity_polling()

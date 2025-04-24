
import os
import telebot
import requests
import pandas as pd
import ta

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

PORTFOLIO_1 = ["BTCUSDT", "ETHUSDT", "AUDIOUSDT", "SOLUSDT", "LINKUSDT", "ATOMUSDT"]
PRICE_API_URL = "https://api.binance.com/api/v3/ticker/24hr?symbol={}"

def get_price_data(symbol):
    try:
        url = PRICE_API_URL.format(symbol)
        response = requests.get(url)
        data = response.json()
        price = round(float(data["lastPrice"]), 2)
        percent = round(float(data["priceChangePercent"]), 2)
        emoji = "📈" if percent > 0 else "📉" if percent < 0 else "➖"
        return f"{price}$ ({emoji} {percent}%)"
    except:
        return "N/A"

def get_technical_analysis(symbol):
    try:
        klines_url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=4h&limit=200"
        df = pd.DataFrame(requests.get(klines_url).json())
        df.columns = ["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"]
        df["close"] = pd.to_numeric(df["close"])
        df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
        df["macd"] = ta.trend.MACD(df["close"]).macd_diff()
        df["ma50"] = df["close"].rolling(window=50).mean()
        df["ma200"] = df["close"].rolling(window=200).mean()
        latest = df.iloc[-1]

        rsi = round(latest["rsi"], 2)
        macd = latest["macd"]
        ma50 = latest["ma50"]
        ma200 = latest["ma200"]
        close = latest["close"]

        rsi_status = "🔴 Surachat" if rsi > 70 else "🟢 Survente" if rsi < 30 else "🟡 RSI neutre"
        macd_status = "📈 MACD positif" if macd > 0 else "📉 MACD négatif"
        ma_status = "📊 Tendance haussière" if ma50 > ma200 else "📊 Tendance baissière" if ma50 < ma200 else "📊 Tendance neutre"

        if rsi > 80:
            signal = "⛔ Vente"
        elif rsi < 30 and macd > 0:
            signal = "✅ Achat"
        else:
            signal = "🔍 Surveillance"

        return rsi, rsi_status, macd_status, ma_status, signal
    except Exception as e:
        return None, "Erreur RSI", "Erreur MACD", "Erreur MA", "❌ Erreur"

@bot.message_handler(commands=["P1"])
def analyse_portfolio_1(message):
    text = "📊 *Analyse Portefeuille 1*
"
    for symbol in PORTFOLIO_1:
        rsi, rsi_status, macd_status, ma_status, signal = get_technical_analysis(symbol)
        price_data = get_price_data(symbol)
        text += f"
{symbol} → {price_data}
{rsi_status} | {macd_status} | {ma_status} | {signal}
"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

bot.polling()

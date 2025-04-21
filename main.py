
import telebot
import requests
import pandas as pd
import ta
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

portfolio_1 = [
    "AAVEUSDT", "ADAUSDT", "ALGOUSDT", "APEUSDT", "ATOMUSDT", "BTCUSDT",
    "DOGEUSDT", "DOTUSDT", "ETHUSDT", "FILUSDT", "GRTUSDT", "HBARUSDT",
    "LINKUSDT", "LTCUSDT", "ONDOUSDT", "PEPEUSDT", "POLUSDT", "RNDRUSDT",
    "SANDUSDT", "SOLUSDT", "UNIUSDT", "XLMUSDT", "XRPUSDT"
]

portfolio_2 = [
    "TAOUSDT", "INJUSDT", "FETUSDT", "CKBUSDT", "KASUSDT", "RSRUSDT",
    "JASMYUSDT", "SHIBUSDT", "PEPEUSDT", "VIRTUALUSDT", "ANKRUSDT",
    "CFXUSDT", "VANAUSDT", "BRETTUSDT", "BONKUSDT", "ARKMUSDT",
    "BICOUSDT", "IMXUSDT", "MOVEUSDT", "BEAMXUSDT", "ATHUSDT",
    "PENGUUSDT", "FLOKIUSDT", "TRUMPUSDT", "AUDIOUSDT"
]

def get_data(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=4h&limit=100"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["close"] = pd.to_numeric(df["close"])
    df["volume"] = pd.to_numeric(df["volume"])
    df["rsi_4h"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    df["macd"] = ta.trend.MACD(df["close"]).macd_diff()
    df["ma50"] = df["close"].rolling(window=50).mean()
    df["ma200"] = df["close"].rolling(window=200).mean()
    return df

def analyze(symbol):
    try:
        df = get_data(symbol)
        rsi = df["rsi_4h"].iloc[-1]
        macd = df["macd"].iloc[-1]
        ma50 = df["ma50"].iloc[-1]
        ma200 = df["ma200"].iloc[-1]
        volume = df["volume"].iloc[-1]
        signal = "🔍 Surveillance"
        if rsi > 70:
            signal = "🔴 Vente (surachat)"
        elif rsi < 30:
            signal = "🟢 Achat (survente)"
        elif macd > 0:
            signal = "🟢 Achat MACD"
        elif macd < 0:
            signal = "🔴 Vente MACD"

        rsi_emoji = "⚠️" if rsi > 70 or rsi < 30 else "✅"
        macd_emoji = "📈" if macd > 0 else "📉"
        ma_trend = "⬆️" if ma50 > ma200 else "⬇️"
        volume_emoji = "📊" if volume > df["volume"].mean() else "💤"

        return f"{symbol} :
{rsi_emoji} RSI 4h : {rsi:.2f}
{macd_emoji} MACD : {macd:.2f}
{ma_trend} MA50/MA200
{volume_emoji} Volume : {volume:.2f}
{signal}
"
    except Exception as e:
        return f"{symbol} : erreur d'analyse"

def analyze_portfolio(portfolio):
    return "\n\n".join([analyze(symbol) for symbol in portfolio])

@bot.message_handler(commands=["P1", "portefeuille1"])
def handle_p1(message):
    bot.send_message(message.chat.id, "Analyse du portefeuille 1 en cours...")
    result = analyze_portfolio(portfolio_1)
    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=["P2"])
def handle_p2(message):
    bot.send_message(message.chat.id, "Analyse du portefeuille 2 en cours...")
    result = analyze_portfolio(portfolio_2)
    bot.send_message(message.chat.id, result)

bot.polling()

import telebot
import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Liste d'exemple portefeuille 1 et 2 (à adapter si besoin)
portfolio_1 = ["BTCUSDT", "ETHUSDT", "AUDIOUSDT", "SOLUSDT", "LINKUSDT", "ATOMUSDT"]
portfolio_2 = ["FETUSDT", "INJUSDT", "SHIBUSDT", "PEPEUSDT", "BONKUSDT"]


def get_crypto_data(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    try:
        response = requests.get(url).json()
        price = float(response["lastPrice"])
        percent = float(response["priceChangePercent"])
        return price, percent
    except:
        return None, None


def format_price_change(percent):
    if percent is None:
        return ""
    arrow = "🔺" if percent > 0 else "🔻"
    return f"{arrow} {percent:.2f}%"


def get_analysis(symbol):
    price, percent = get_crypto_data(symbol)
    rsi = 50 + (hash(symbol) % 50 - 25)  # Simulation
    macd_pos = hash(symbol) % 2 == 0
    trend = "neutre"

    status = "🔍 Surveillance"
    rsi_status = "🟡 RSI neutre"
    if rsi > 70:
        rsi_status = "🔴 Surachat"
        status = "🛑 Vente"
    elif rsi < 30:
        rsi_status = "🟢 Survente"
        status = "🟩 Achat"

    macd_status = "📉 MACD négatif" if not macd_pos else "📈 MACD positif"
    trend_status = "📊 Tendance neutre"

    price_part = f"💰 {price:.4f} USD" if price else ""
    change_part = format_price_change(percent)

    return f"{symbol} → RSI {rsi:.2f} | {rsi_status} | {macd_status} | {trend_status} | {price_part} {change_part} | {status}"


def build_message(title, symbols):
    text = f"📊 *{title}*\n\n"
    for sym in symbols:
        text += get_analysis(sym) + "\n\n"
    return text


@bot.message_handler(commands=['P1'])
def portefeuille1_handler(message):
    text = build_message("Analyse Portefeuille 1", portfolio_1)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(commands=['P2'])
def portefeuille2_handler(message):
    text = build_message("Analyse Portefeuille 2", portfolio_2)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


print("🤖 Bot prêt à l'analyse complète...")
bot.polling()

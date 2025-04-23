import os
import telebot
from utils import get_crypto_data, format_crypto_display, get_portfolio_1, get_portfolio_2, get_signals, get_extreme_rsi, get_total_summary

# Protection d'accès
AUTHORIZED_USER_ID = 5765277693

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Vérification d'accès
def is_authorized(message):
    return message.from_user.id == AUTHORIZED_USER_ID

@bot.message_handler(commands=['P1', 'portefeuille1'])
def handle_p1(message):
    if not is_authorized(message):
        return
    data = get_portfolio_1()
    for line in data:
        bot.send_message(message.chat.id, line)

@bot.message_handler(commands=['P2'])
def handle_p2(message):
    if not is_authorized(message):
        return
    data = get_portfolio_2()
    for line in data:
        bot.send_message(message.chat.id, line)

@bot.message_handler(commands=['S'])
def handle_signals(message):
    if not is_authorized(message):
        return
    signals = get_signals()
    if signals:
        text = "*📊 Signaux d'achat/vente détectés :*\n\n" + "\n\n".join(signals)
    else:
        text = "⚠️ Aucun signal d'achat ou de vente détecté pour le moment."
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['SS'])
def handle_extremes(message):
    if not is_authorized(message):
        return
    alerts = get_extreme_rsi()
    if alerts:
        text = "*📈 Cryptos en surachat ou survente :*\n\n" + "\n\n".join(alerts)
    else:
        text = "ℹ️ Aucune crypto actuellement en surachat ou survente."
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['tot'])
def handle_tot(message):
    if not is_authorized(message):
        return
    summary = get_total_summary()
    bot.send_message(message.chat.id, summary, parse_mode="Markdown")

bot.polling()

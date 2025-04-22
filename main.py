
import telebot
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

portfolio_1 = ["BTCUSDT", "ETHUSDT", "AUDIOUSDT", "SOLUSDT", "LINKUSDT", "ATOMUSDT", "ADAUSDT", "MATICUSDT", "DOTUSDT"]
portfolio_2 = ["FETUSDT", "INJUSDT", "JASMYUSDT", "CKBUSDT", "KASUSDT", "RSRUSDT", "PEPEUSDT", "VIRTUALUSDT", "ANKRUSDT", "CFXUSDT", "VANAUSDT", "BRETTUSDT", "BONKUSDT", "ARKMUSDT", "BICOUSDT", "IMXUSDT", "MOVEUSDT", "BEAMXUSDT", "RNDRUSDT", "PENGUUSDT", "ATHUSDT", "FLOKIUSDT", "TRUMPUSDT", "AAVEUSDT", "TAOUSDT", "SHIBUSDT", "XLMUSDT", "XRPUSDT", "UNIUSDT"]

@bot.message_handler(commands=['P1'])
def portefeuille1(message):
    text = "*📊 Analyse Portefeuille 1*"
    for sym in portfolio_1:
        text += f"\n\n{sym} → RSI 50.00"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['P2'])
def portefeuille2(message):
    text = "*📊 Analyse Portefeuille 2*"
    for sym in portfolio_2:
        text += f"\n\n{sym} → RSI 50.00"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

bot.polling()

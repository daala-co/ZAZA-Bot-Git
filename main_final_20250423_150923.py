# main.py - Fichier final optimisé avec affichage structuré

import telebot
from utils import get_crypto_data, format_crypto_display

BOT_TOKEN = "TON_TOKEN_ICI"
bot = telebot.TeleBot(BOT_TOKEN)

AUTHORIZED_USERS = [123456789]  # Remplacer par ton ID Telegram

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Bienvenue ! Tape /P1 ou /P2 pour analyser ton portefeuille.")

@bot.message_handler(commands=['P1'])
def analyse_portefeuille1(message):
    if message.chat.id not in AUTHORIZED_USERS:
        return bot.reply_to(message, "⛔ Accès refusé.")
    response = format_crypto_display("P1")
    bot.reply_to(message, response)

@bot.message_handler(commands=['P2'])
def analyse_portefeuille2(message):
    if message.chat.id not in AUTHORIZED_USERS:
        return bot.reply_to(message, "⛔ Accès refusé.")
    response = format_crypto_display("P2")
    bot.reply_to(message, response)

@bot.message_handler(commands=['S'])
def analyse_signaux(message):
    if message.chat.id not in AUTHORIZED_USERS:
        return bot.reply_to(message, "⛔ Accès refusé.")
    response = format_crypto_display("SIGNAL")
    bot.reply_to(message, response or "❗ Aucun signal d'achat ou de vente clair pour l'instant.")

@bot.message_handler(commands=['SS'])
def analyse_surachat_survente(message):
    if message.chat.id not in AUTHORIZED_USERS:
        return bot.reply_to(message, "⛔ Accès refusé.")
    response = format_crypto_display("SURVEILLANCE")
    bot.reply_to(message, response or "❗ Aucune crypto actuellement en surachat ou survente.")

if __name__ == "__main__":
    bot.polling()

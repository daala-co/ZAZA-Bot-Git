import os
import telebot

AUTHORIZED_USER_ID = 5765277693
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

def is_authorized(message):
    return message.from_user.id == AUTHORIZED_USER_ID

@bot.message_handler(commands=['start', 'test'])
def handle_start(message):
    if not is_authorized(message):
        return
    bot.send_message(message.chat.id, "✅ Bot démarré avec succès !")

bot.polling()

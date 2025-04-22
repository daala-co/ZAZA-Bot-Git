
import telebot
import requests

BOT_TOKEN = "TON_TOKEN_ICI"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "✅ Bot crypto actif avec analyse complète.")

# Exemple de réponse à /P1
@bot.message_handler(commands=['P1'])
def portefeuille1(message):
    text = (
        "📦 *Portefeuille 1 – Analyse Complète*

"
        "🧠 *Layer 1 / Smart Contracts*
"
        "*Bitcoin (BTCUSDT)* – 66 500 $ 📈 (+2.1%)
"
        "📊 RSI (1D): 54 ⚪️ – RSI (4H): 61 ⚪️
"
        "💹 MACD: 🔽 Bearish
"
        "📏 MA50/200: ⚠️ Croisement possible
"
        "📉 Statut: 👁️ Surveillance

"
        "*Ethereum (ETHUSDT)* – 3 250 $ 📉 (−0.9%)
"
        "📊 RSI (1D): 47 ⚪️ – RSI (4H): 42 🟥
"
        "💹 MACD: 🔽 Bearish
"
        "📏 MA50/200: ❌
"
        "📉 Statut: 🔻 Vente potentielle

"
        "🎨 *Metaverse / NFT*
"
        "*Render (RENDERUSDT)* – 10.45 $ 📈 (+1.6%)
"
        "📊 RSI (1D): 68 🔵 – RSI (4H): 74 🔵
"
        "💹 MACD: 🔼 Bullish
"
        "📏 MA50/200: ✅
"
        "📈 Statut: 🟢 Signal d'achat

"
        "🐶 *Meme / Communautaire*
"
        "*Dogecoin (DOGEUSDT)* – 0.161 $ 📈 (+5.2%)
"
        "📊 RSI (1D): 72 🔵 – RSI (4H): 79 🔵
"
        "💹 MACD: 🔼 Bullish
"
        "📏 MA50/200: ✅
"
        "📈 Statut: 🚀 Fort achat

"
        "📊 *Résumé du Portefeuille 1*
"
        "💰 *Valeur totale estimée :* 15 670 CHF (≈ 17 300 USD)
"
        "📈 *Évolution 24h :* +2.8%
"
        "📈 *Top hausses :*
"
        "1. DOGEUSDT 🟢 +5.2%
"
        "2. ADAUSDT 🟢 +3.8%
"
        "3. RENDERUSDT 🟢 +1.6%

"
        "📉 *Top baisses :*
"
        "1. ETHUSDT 🔻 −0.9%
"
        "2. SANDUSDT 🔻 −0.5%
"
        "3. UNIUSDT 🔻 −0.3%

"
        "📌 *Signaux d'achat :* 3 🟢
"
        "📌 *Signaux de vente :* 1 🔻
"
        "📌 *Neutres / surveillance :* 7 👁️"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# Lancement du bot
bot.polling()

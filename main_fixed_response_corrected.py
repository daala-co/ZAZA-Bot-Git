
# ... début du fichier (importations, setup du bot, définitions des listes P1/P2, etc.)
# Les parties précédentes du code restent inchangées

@bot.message_handler(commands=['S'])
def handle_signals(message):
    signals = []
    for symbol in portfolio1 + portfolio2:
        rsi = get_rsi(symbol)
        macd = get_macd(symbol)
        if rsi > 70 or rsi < 30 or macd['signal'] != "neutre":
            signals.append(build_analysis(symbol))
    if not signals:
        signals.append("❌ Aucun signal d'achat ou de vente détecté.")
    text = "\n\n".join(signals)
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['SS'])
def handle_overbought_oversold(message):
    messages = []
    for symbol in portfolio1 + portfolio2:
        rsi = get_rsi(symbol)
        if rsi > 70 or rsi < 30:
            messages.append(build_analysis(symbol))
    if not messages:
        messages.append("🔍 Aucune crypto en surachat ou survente.")
    text = "\n\n".join(messages)
    bot.send_message(message.chat.id, text)

# ... fin du fichier, fonctions existantes inchangées

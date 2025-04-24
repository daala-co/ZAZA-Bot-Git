import requests

# --- CONFIGURATION DES PORTEFEUILLES ---
PORTFOLIO_1 = [
    'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'LINKUSDT', 'DOTUSDT',
    'ADAUSDT', 'MATICUSDT', 'DOGEUSDT', 'ATOMUSDT', 'AAVEUSDT',
    'APEUSDT', 'FILUSDT', 'GRTUSDT', 'HBARUSDT', 'LTCUSDT',
    'ONDOUSDT', 'POLUSDT', 'RENDERUSDT', 'SANDUSDT', 'UNIUSDT',
    'XLMUSDT', 'XRPUSDT'
]
PORTFOLIO_2 = [
    'TAOUSDT', 'INJUSDT', 'FETUSDT', 'CKBUSDT', 'KASUSDT',
    'RSRUSDT', 'JASMYUSDT', 'SHIBUSDT', 'PEPEUSDT', 'VIRTUALUSDT',
    'ANKRUSDT', 'CFXUSDT', 'VANAUSDT', 'BRETTUSDT', 'BONKUSDT',
    'ARKMUSDT', 'BICOUSDT', 'IMXUSDT', 'MOVEUSDT', 'BEAMXUSDT',
    'PENGUUSDT', 'TRUMPUSDT', 'AUDIOUSDT'
]

# --- OUTILS POUR TRI PAR CAPITALISATION (ordre simulé) ---
CAP_ORDER = {
    'BTCUSDT': 1,  'ETHUSDT': 2,  'BNBUSDT': 3,  'SOLUSDT': 4,  'XRPUSDT': 5,  'DOGEUSDT': 6,
    'ADAUSDT': 7,  'AVAXUSDT': 8, 'DOTUSDT': 9,  'LINKUSDT': 10, 'TRXUSDT': 11, 'MATICUSDT': 12,
    'ATOMUSDT': 13, 'LTCUSDT': 14, 'UNIUSDT': 15, 'IMXUSDT': 16, 'INJUSDT': 17, 'RENDERUSDT': 18,
    'FILUSDT': 19, 'HBARUSDT': 20, 'APEUSDT': 21, 'PEPEUSDT': 22, 'SHIBUSDT': 23, 'FETUSDT': 24,
    'KASUSDT': 25, 'AAVEUSDT': 26, 'ARKMUSDT': 27, 'SANDUSDT': 28, 'VANAUSDT': 29, 'VIRTUALUSDT': 30,
    'TAOUSDT': 31, 'CFXUSDT': 32, 'POLUSDT': 33, 'JASMYUSDT': 34, 'RSRUSDT': 35, 'XLMUSDT': 36,
    'BEAMXUSDT': 37, 'GRTUSDT': 38, 'ANKRUSDT': 39, 'BONKUSDT': 40, 'MOVEUSDT': 41, 'BICOUSDT': 42,
    'TRUMPUSDT': 43, 'ONDOUSDT': 44, 'CKBUSDT': 45, 'AUDIOUSDT': 46, 'PENGUUSDT': 47, 'BRETTUSDT': 48
}

# --- RÉCUPÉRATION DES DONNÉES ---
def get_crypto_data(symbol):
    """Récupère le prix actuel et la variation 24h depuis l'API Binance."""
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        res = requests.get(url)
        data = res.json()
        price = float(data['lastPrice'])
        change = float(data['priceChangePercent'])
        return price, change
    except:
        return None, None

# --- FORMATAGE D'UNE CRYPTO ---
def format_crypto_display(name, symbol, price, change, rsi_4h, rsi_1d, macd, trend, ma50, ma200, support, resistance, volume, status):
    formatted = (
        f"🔵 *{name.upper()} ({symbol})*\n"
        f"💰 Prix actuel : {price:.4f} $ {'🔺' if change >= 0 else '🔻'} {abs(change):.2f}%\n"
        f"📊 RSI 4h : {rsi_4h:.2f} {'🟢' if rsi_4h < 30 else '🔴' if rsi_4h > 70 else '🟠'}\n"
        f"📊 RSI 1D : {rsi_1d:.2f} {'🟢' if rsi_1d < 30 else '🔴' if rsi_1d > 70 else '🟠'}\n"
        f"📈 MACD : {'🔼 Haussier' if macd == 'bullish' else '🔽 Baissier'}\n"
        f"📊 Tendance : {'Haussière 🔼' if trend == 'haussière' else 'Baissière 🔽' if trend == 'baissière' else 'Neutre'}\n"
        f"📏 MA50 : {ma50:.4f} / MA200 : {ma200:.4f} {'🔼' if ma50 > ma200 else '🔽'}\n"
        f"📉 Support : {support:.4f} / Résistance : {resistance:.4f}\n"
        f"📦 Volume : {volume}\n"
        f"📌 Statut : {status}"
    )
    return formatted

# --- TRI PAR CAPITALISATION ---
def sort_by_capitalization(symbols):
    """Trie une liste de symboles selon l'ordre de capitalisation défini."""
    return sorted(symbols, key=lambda s: CAP_ORDER.get(s, 999))

# --- ANALYSE DES INDICATEURS ---
import hashlib

# Noms clairs des cryptos pour affichage
NAMES = {
    'BTC': 'Bitcoin',    'ETH': 'Ethereum',   'BNB': 'Binance Coin', 'SOL': 'Solana',   'XRP': 'XRP',
    'DOGE': 'Dogecoin',  'ADA': 'Cardano',    'AVAX': 'Avalanche',   'DOT': 'Polkadot', 'LINK': 'Chainlink',
    'TRX': 'TRON',       'MATIC': 'Polygon',  'ATOM': 'Cosmos',      'LTC': 'Litecoin', 'UNI': 'Uniswap',
    'IMX': 'ImmutableX', 'INJ': 'Injective',  'RENDER': 'Render',    'FIL': 'Filecoin', 'HBAR': 'Hedera',
    'APE': 'ApeCoin',    'PEPE': 'Pepe',      'SHIB': 'Shiba Inu',   'FET': 'Fetch.ai', 'KAS': 'Kaspa',
    'AAVE': 'Aave',      'ARKM': 'Arkham',    'SAND': 'Sandbox',     'VANA': 'Nirvana', 'VIRTUAL': 'Virtuals Protocol',
    'TAO': 'Bittensor',  'CFX': 'Conflux',    'POL': 'Polygon',      'JASMY': 'Jasmy',  'RSR': 'Reserve Rights',
    'XLM': 'Stellar',    'BEAMX': 'Beam',     'GRT': 'Graph',        'ANKR': 'Ankr',    'BONK': 'Bonk',
    'MOVE': 'Movement',  'BICO': 'Biconomy',  'TRUMP': 'Trump',      'ONDO': 'Ondo',    'CKB': 'Nervos',
    'AUDIO': 'Audius',   'PENGU': 'Pudgy Penguins', 'BRETT': 'Brett'
}

def deterministic_value(key: str, modulo: int):
    """Génère de façon déterministe une valeur entière à partir d'une clé donnée."""
    h = hashlib.sha256(key.encode()).hexdigest()
    val = int(h[:8], 16)
    return val % modulo if modulo else val

def analyze_symbol(symbol):
    """Analyse un symbole et renvoie toutes les données formatées nécessaires."""
    price, change = get_crypto_data(symbol)
    if price is None or change is None:
        return None  # Données indisponibles
    base_symbol = symbol.replace('USDT', '')
    name = NAMES.get(base_symbol, base_symbol)
    # Indicateurs techniques simulés
    rsi_4h = deterministic_value(symbol + "_4h", 101)
    rsi_1d = deterministic_value(symbol + "_1d", 101)
    macd = 'bullish' if deterministic_value(symbol + "_macd", 2) == 0 else 'bearish'
    # Moyennes mobiles simulées (MA50 et MA200)
    if macd == 'bullish':
        ma50 = price * 1.03
        ma200 = price * 0.95
    else:
        ma50 = price * 0.97
        ma200 = price * 1.05
    # Supports et résistances simulés (~±10% du prix)
    sup_offset = deterministic_value(symbol + "_sup", 5)  # entier 0-4
    res_offset = deterministic_value(symbol + "_res", 5)  # entier 0-4
    support = price * (0.90 + 0.02 * sup_offset)
    resistance = price * (1.02 + 0.02 * res_offset)
    # Volume (léger/moyen/fort) selon la taille de la crypto
    rank = CAP_ORDER.get(symbol, 999)
    if rank <= 16:
        volume = "fort"
    elif rank <= 32:
        volume = "moyen"
    else:
        volume = "léger"
    # Statut d'action (Achat/Vente/Surveillance) basé sur RSI extrêmes
    if rsi_4h < 30 or rsi_1d < 30:
        status = "🟢 Achat"
    elif rsi_4h > 70 or rsi_1d > 70:
        status = "🔴 Vente"
    else:
        status = "🟡 Surveillance"
    # Tendance générale (neutre par défaut, haussière/baissière si signaux concordants)
    if change >= 1 and macd == 'bullish' and ma50 > ma200:
        trend = "haussière"
    elif change <= -1 and macd == 'bearish' and ma50 < ma200:
        trend = "baissière"
    else:
        trend = "neutre"
    return name, base_symbol, price, change, rsi_4h, rsi_1d, macd, trend, ma50, ma200, support, resistance, volume, status

# --- FONCTIONS PRINCIPALES DU BOT ---
def get_portfolio_1():
    """Retourne la liste des analyses formatées pour chaque crypto du Portefeuille 1."""
    symbols = sort_by_capitalization(PORTFOLIO_1)
    lines = []
    for sym in symbols:
        data = analyze_symbol(sym)
        if data:
            # Déballer les données et formater la ligne d'affichage
            name, base_symbol, price, change, rsi_4h, rsi_1d, macd, trend, ma50, ma200, support, resistance, volume, status = data
            lines.append(format_crypto_display(name, base_symbol, price, change, rsi_4h, rsi_1d, macd, trend, ma50, ma200, support, resistance, volume, status))
    return lines

def get_portfolio_2():
    """Retourne la liste des analyses formatées pour chaque crypto du Portefeuille 2."""
    symbols = sort_by_capitalization(PORTFOLIO_2)
    lines = []
    for sym in symbols:
        data = analyze_symbol(sym)
        if data:
            name, base_symbol, price, change, rsi_4h, rsi_1d, macd, trend, ma50, ma200, support, resistance, volume, status = data
            lines.append(format_crypto_display(name, base_symbol, price, change, rsi_4h, rsi_1d, macd, trend, ma50, ma200, support, resistance, volume, status))
    return lines

def get_signals():
    """Retourne les cryptos qui ont un signal d'achat ou de vente (RSI extrêmes)."""
    symbols = sort_by_capitalization(PORTFOLIO_1 + PORTFOLIO_2)
    signals_list = []
    for sym in symbols:
        data = analyze_symbol(sym)
        if data:
            name, base_symbol, *_, status = data
            if status.startswith("🟢") or status.startswith("🔴"):
                signals_list.append(f"{name.upper()} ({base_symbol}) {status}")
    return signals_list

def get_extreme_rsi():
    """Retourne les cryptos en situation de surachat ou de survente."""
    symbols = sort_by_capitalization(PORTFOLIO_1 + PORTFOLIO_2)
    alerts = []
    for sym in symbols:
        data = analyze_symbol(sym)
        if data:
            name, base_symbol, _, _, rsi_4h, rsi_1d, *rest = data
            if rsi_4h > 70 or rsi_1d > 70:
                alerts.append(f"{name.upper()} ({base_symbol}) 🔴 Surachat")
            elif rsi_4h < 30 or rsi_1d < 30:
                alerts.append(f"{name.upper()} ({base_symbol}) 🟢 Survente")
    return alerts

def get_total_summary():
    """Retourne un résumé global du portefeuille (valeur totale, performance, top hausses/baisses)."""
    symbols = sort_by_capitalization(PORTFOLIO_1 + PORTFOLIO_2)
    # On suppose un investissement initial de 100$ par crypto pour simuler la performance
    initial_value_per_coin = 100.0
    initial_total = len(symbols) * initial_value_per_coin
    current_total = 0.0
    performance_data = []
    for sym in symbols:
        price, change = get_crypto_data(sym)
        if price is None or change is None:
            continue
        # Valeur actuelle si 100$ investis initialement dans cette crypto
        current_value = initial_value_per_coin * (1 + change / 100.0)
        current_total += current_value
        performance_data.append((sym, change))
    total_value_usd = current_total
    total_value_chf = total_value_usd * 0.90  # Conversion approximative en CHF
    gain_percent = 0.0
    if initial_total > 0:
        gain_percent = (current_total - initial_total) / initial_total * 100.0
    # Top 3 hausses et baisses (par variation 24h en %)
    performance_data.sort(key=lambda x: x[1], reverse=True)
    top_gainers = performance_data[:3]
    performance_data.sort(key=lambda x: x[1])
    top_losers = performance_data[:3]
    # Construction du résumé
    summary_lines = []
    summary_lines.append("*📊 Résumé global du portefeuille :*")
    summary_lines.append(f"Valeur totale : {total_value_usd:.2f} $ (~{total_value_chf:.2f} CHF)")
    summary_lines.append(f"Performance totale : {'+' if gain_percent >= 0 else ''}{gain_percent:.2f}%")
    if top_gainers:
        gains_text = ", ".join([f"{sym.replace('USDT','')} ({'+' if chg >= 0 else ''}{chg:.2f}%)" for sym, chg in top_gainers])
        summary_lines.append("Top 3 hausses : " + gains_text)
    if top_losers:
        losses_text = ", ".join([f"{sym.replace('USDT','')} ({'+' if chg >= 0 else ''}{chg:.2f}%)" for sym, chg in top_losers])
        summary_lines.append("Top 3 baisses : " + losses_text)
    return "\n".join(summary_lines)

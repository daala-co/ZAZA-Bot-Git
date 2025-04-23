import requests
from operator import itemgetter

# --- CONFIGURATION DES PORTEFEUILLES ---
def get_portfolio_1():
    return [
        'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'LINKUSDT', 'DOTUSDT',
        'ADAUSDT', 'MATICUSDT', 'DOGEUSDT', 'ATOMUSDT', 'AAVEUSDT',
        'APEUSDT', 'FILUSDT', 'GRTUSDT', 'HBARUSDT', 'LTCUSDT',
        'ONDOUSDT', 'POLUSDT', 'RNDRUSDT', 'SANDUSDT', 'UNIUSDT',
        'XLMUSDT', 'XRPUSDT'
    ]

def get_portfolio_2():
    return [
        'TAOUSDT', 'INJUSDT', 'FETUSDT', 'CKBUSDT', 'KASUSDT',
        'RSRUSDT', 'JASMYUSDT', 'SHIBUSDT', 'PEPEUSDT', 'VIRTUALUSDT',
        'ANKRUSDT', 'CFXUSDT', 'VANAUSDT', 'BRETTUSDT', 'BONKUSDT',
        'ARKMUSDT', 'BICOUSDT', 'IMXUSDT', 'MOVEUSDT', 'BEAMXUSDT',
        'PENGUUSDT', 'TRUMPUSDT', 'AUDIOUSDT'
    ]

# --- OUTILS POUR TRI PAR CAPITALISATION (ordre simulé) ---
CAP_ORDER = {
    'BTCUSDT': 1, 'ETHUSDT': 2, 'BNBUSDT': 3, 'SOLUSDT': 4, 'XRPUSDT': 5, 'DOGEUSDT': 6,
    'ADAUSDT': 7, 'AVAXUSDT': 8, 'DOTUSDT': 9, 'LINKUSDT': 10, 'TRXUSDT': 11,
    'MATICUSDT': 12, 'ATOMUSDT': 13, 'LTCUSDT': 14, 'UNIUSDT': 15, 'IMXUSDT': 16,
    'INJUSDT': 17, 'RNDRUSDT': 18, 'FILUSDT': 19, 'HBARUSDT': 20, 'APEUSDT': 21,
    'PEPEUSDT': 22, 'SHIBUSDT': 23, 'FETUSDT': 24, 'KASUSDT': 25, 'AAVEUSDT': 26,
    'ARKMUSDT': 27, 'SANDUSDT': 28, 'VANAUSDT': 29, 'VIRTUALUSDT': 30, 'TAOUSDT': 31,
    'CFXUSDT': 32, 'POLUSDT': 33, 'JASMYUSDT': 34, 'RSRUSDT': 35, 'XLMUSDT': 36,
    'BEAMXUSDT': 37, 'GRTUSDT': 38, 'ANKRUSDT': 39, 'BONKUSDT': 40, 'MOVEUSDT': 41,
    'BICOUSDT': 42, 'TRUMPUSDT': 43, 'ONDOUSDT': 44, 'CKBUSDT': 45, 'AUDIOUSDT': 46,
    'PENGUUSDT': 47, 'BRETTUSDT': 48
}

# --- Récupération et Formatage ---
def get_crypto_data(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        res = requests.get(url)
        data = res.json()
        price = float(data['lastPrice'])
        change = float(data['priceChangePercent'])
        return price, change
    except:
        return None, None

def format_crypto_display(name, symbol, price, change, rsi_4h, rsi_1d, macd, trend, ma50, ma200, support, resistance, volume, status):
    formatted = (
        f"\n🔵 *{name.upper()} ({symbol})*\n"
        f"💰 Prix actuel : {price:.4f} $ {'🔺' if change >= 0 else '🔻'} {abs(change):.2f}%\n"
        f"📊 RSI 4h : {rsi_4h} {'🟢' if rsi_4h < 30 else '🔴' if rsi_4h > 70 else '🟠'}\n"
        f"📊 RSI 1D : {rsi_1d} {'🟢' if rsi_1d < 30 else '🔴' if rsi_1d > 70 else '🟠'}\n"
        f"📈 MACD : {'🔼 Haussier' if macd == 'bullish' else '🔽 Baissier'}\n"
        f"📏 MA50 : {ma50} / MA200 : {ma200} {'🔼' if ma50 > ma200 else '🔽'}\n"
        f"📉 Support : {support} / Résistance : {resistance}\n"
        f"📦 Volume : {volume}\n"
        f"📌 Statut : {status}"
    )
    return formatted

# --- Fonctions pour tri ---
def sort_by_capitalization(symbols):
    return sorted(symbols, key=lambda s: CAP_ORDER.get(s, 999))

# --- Fonctions pour filtres ---
def get_signals(all_symbols):
    return [s for s in all_symbols if hash(s) % 3 == 0]  # Simule un signal

def get_extreme_rsi(all_symbols):
    return [s for s in all_symbols if hash(s) % 5 == 0]  # Simule surachat/survente

def get_total_summary(portfolio_1, portfolio_2):
    all_ = portfolio_1 + portfolio_2
    total_value = len(all_) * 100  # Simulé
    gain = 12.3
    top_gains = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']
    top_losses = ['APEUSDT', 'PEPEUSDT', 'FILUSDT']
    return total_value, gain, top_gains, top_losses

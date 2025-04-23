
import requests

def get_crypto_data(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def format_crypto_display(name, symbol, data, rsi_4h, rsi_1d, macd, ma50, ma200, support, resistance, volume, status):
    price = float(data.get("lastPrice", 0))
    change = float(data.get("priceChangePercent", 0))
    
    price_color = "🟢" if change >= 0 else "🔻"
    status_line = f"📌 Statut : {status}"

    formatted = (
        f"🔵 *{name.upper()} ({symbol})*
"
        f"💰 Prix actuel : {price:.3f} $ {price_color} {change:.2f}%
"
        f"📊 RSI 4h : {rsi_4h} {get_rsi_emoji(rsi_4h)}
"
        f"📊 RSI 1D : {rsi_1d} {get_rsi_emoji(rsi_1d)}
"
        f"📈 MACD : {get_macd_emoji(macd)} {macd}
"
        f"📏 MA50 : {ma50} / MA200 : {ma200} {get_ma_trend(ma50, ma200)}
"
        f"📉 Support : {support} / Résistance : {resistance}
"
        f"📦 Volume : {volume}
"
        f"{status_line}
"
    )
    return formatted

def get_rsi_emoji(value):
    if value >= 70:
        return "🔴"
    elif value <= 30:
        return "🟢"
    else:
        return "🟠"

def get_macd_emoji(value):
    return "🔼" if "positif" in value.lower() else "🔽"

def get_ma_trend(ma50, ma200):
    return "🔼" if ma50 > ma200 else "🔽"

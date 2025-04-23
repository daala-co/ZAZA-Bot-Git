
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
        return (
    f"🔵 *{name.upper()} ({symbol})*\n"
    f"💰 Prix actuel : {price} $ {'🔺' if price_change >= 0 else '🔻'} {price_change_percent}%\n"
    f"📊 RSI 4h : {rsi_4h} {rsi_4h_icon}\n"
    f"📊 RSI 1D : {rsi_1d} {rsi_1d_icon}\n"
    f"📈 MACD : {macd_icon} {macd_trend}\n"
    f"📏 MA50 : {ma_50} / MA200 : {ma_200} {ma_trend}\n"
    f"📉 Support : {support} / Résistance : {resistance}\n"
    f"📦 Volume : {volume_level}\n"
    f"📌 Statut : {status_icon} {status}"
)
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

import requests
import pandas as pd
from datetime import datetime
import os
from telegram_notifier import send_telegram_message

def get_usdt_symbols():
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    r = requests.get(url).json()
    return [item["symbol"] for item in r if item["symbol"].endswith("USDT")]

def get_binance_price(symbol):
    url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
    return float(requests.get(url).json()["price"])

def get_funding_rate(symbol):
    url = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&limit=1"
    return float(requests.get(url).json()[0]["fundingRate"])

def get_open_interest(symbol):
    url = f"https://fapi.binance.com/futures/data/openInterestHist?symbol={symbol}&period=5m&limit=1"
    r = requests.get(url).json()
    return float(r[0]["sumOpenInterest"]) if r else None

def collect_data():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    symbols = get_usdt_symbols()
    rows = []

    for symbol in symbols:
        try:
            price = get_binance_price(symbol)
            fr = get_funding_rate(symbol)
            oi = get_open_interest(symbol)
            rows.append([now, symbol, price, fr, oi])
        except Exception as e:
            send_telegram_message(f"❌ {symbol} Hatası: {e}")

    df = pd.DataFrame(rows, columns=["timestamp", "symbol", "price", "funding_rate", "open_interest"])
    file_path = "data/market_data.csv"
    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path)
        df = pd.concat([df_existing, df], ignore_index=True)
    df.to_csv(file_path, index=False)

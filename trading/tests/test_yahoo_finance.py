import pytest
from datetime import datetime
from ..models.Services.yahoo_finance import YahooFinance

def test_get_price():
    yf = YahooFinance()
    assert yf.get_price("AAPL") > 0

def test_get_price_invalid():
    yf = YahooFinance()
    assert yf.get_price("INVALID") == -1
    assert yf.get_price("AAPL") > 0
    assert yf.get_price("dkake") == -1

def test_get_btc_price():
    yf = YahooFinance()
    btc_price = yf.get_price("BTC-USD")
    print(f"BTC-USD price: {btc_price}")
    assert btc_price > 0

def test_get_canadian_price():
    yf = YahooFinance()
    ry_price = yf.get_price("RY.TO")
    print(f"RY.TO price: {ry_price}")
    assert ry_price > 0

def test_get_tickers_price():
    yf = YahooFinance()
    symbols = ["AAPL", "GOOGL", "INVALID","RY.TO","ETH-USD"]
    prices = yf.get_tickers_price(symbols)
    assert prices["AAPL"] > 0
    assert prices["GOOGL"] > 0
    assert prices["INVALID"] == -1
    assert prices["RY.TO"] > 0
    assert prices["ETH-USD"] > 0
    print(f"Prices: {prices}")
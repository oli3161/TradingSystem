import yfinance as yf
from .asset_price_service import AssetPriceService

class YahooFinance(AssetPriceService):

    def get_price(self, asset_symbol: str) -> float:
        try:
            ticker = yf.Ticker(asset_symbol)
            history = ticker.history(period="1d")
            if history.empty:
                raise ValueError(f"No data found for symbol: {asset_symbol}")
            price = history['Close'].iloc[0]
            rounded_price = round(price, 2)
            return rounded_price
        except ValueError as ve:
            print(f"ValueError: {ve}")
            return -1
        except Exception as e:
            print(f"An error occurred: {e}")
            return -1

    def get_tickers_price(self, asset_symbols: list) -> dict:
        try:
            tickers = yf.Tickers(' '.join(asset_symbols))
            prices = {}
            for symbol in asset_symbols:
                history = tickers.tickers[symbol].history(period="1d")
                if history.empty:
                    prices[symbol] = -1
                else:
                    price = history['Close'].iloc[0]
                    rounded_price = round(price, 2)
                    prices[symbol] = float(rounded_price)
            return prices
        except Exception as e:
            print(f"An error occurred: {e}")
            return {symbol: -1 for symbol in asset_symbols}
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
        prices = {}
        try:
            tickers = yf.Tickers(' '.join(asset_symbols))
            for symbol in asset_symbols:
                try:
                    # Essayez de récupérer l'historique pour le symbole donné
                    history = tickers.tickers[symbol].history(period="1d")
                    if history.empty:
                        # Si l'historique est vide, retournez -1 pour ce symbole
                        prices[symbol] = -1
                    else:
                        # Récupérez le prix de clôture et arrondissez-le
                        price = history['Close'].iloc[0]
                        rounded_price = round(price, 2)
                        prices[symbol] = float(rounded_price)
                except Exception as e:
                    # En cas d'erreur pour un symbole, loggez l'erreur et retournez -1 pour ce symbole
                    print(f"Error fetching price for symbol {symbol}: {e}")
                    prices[symbol] = -1
        except Exception as e:
            # Si une erreur générale survient, loggez l'erreur et retournez -1 pour tous les symboles
            print(f"An error occurred while processing tickers: {e}")
            return {symbol: -1 for symbol in asset_symbols}
        return prices

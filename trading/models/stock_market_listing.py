from mypy_extensions import NoReturn
from typing import Union
class StockMarketListing:

    def __init__(self, ticker_symbol: str, company_name: Union[float, str], last_price: float) -> NoReturn:
        self.ticker_symbol = ticker_symbol
        self.company_name = company_name
        self.bid_price = last_price
        self.ask_price = last_price
        self.last_price = last_price

    def update_price(self, price: float) -> NoReturn:

        self.last_price = price

    def update_bid_price(self, price: float) -> NoReturn:
        self.bid_price = price

    def update_ask_price(self, price: float) -> NoReturn:
        self.ask_price = price

    def __str__(self):
        return f"Ticker: {self.ticker_symbol} Company: {self.company_name} Last Price: {self.last_price} Bid Price: {self.bid_price} Ask Price: {self.ask_price}"

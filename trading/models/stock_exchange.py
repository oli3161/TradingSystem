from typing import Dict
from trading.models.market_maker import MarketMaker
from trading.models.order import Order
from trading.models.order_matching_engine import OrderMatchingEngine
from trading.models.stock_market_listing import StockMarketListing
from mypy_extensions import NoReturn


class StockExchange:

    def __init__(self, name: str) -> NoReturn:
        self.name = name
        self.stock_market_listings: Dict[str, StockMarketListing] = {}
        self.stock_marketMakers: Dict[str, MarketMaker] = {}

    def submit_order(self, order: Order):

        stock_market_listing: MarketMaker = self.stock_marketMakers.get(
            order.ticker, "Key not found"
        )

        stock_market_listing.process_order(order)

    def getMarketMaker(self, ticker_symbol) -> MarketMaker:
        return self.stock_marketMakers.get(ticker_symbol, "Key not found")

    def addStockMarketListing(self, ticker_symbol: str, company_name: str, last_price: float) -> NoReturn:

        stock_market_listing = StockMarketListing(
            ticker_symbol, company_name, last_price
        )

        order_matching_engine = OrderMatchingEngine(stock_market_listing)
        marketMaker = MarketMaker(
            order_matching_engine, ticker_symbol, stock_market_listing
        )

        self.stock_marketMakers[ticker_symbol] = marketMaker

        self.stock_market_listings[stock_market_listing.ticker_symbol] = (
            stock_market_listing
        )

    def match_orders(self):

        for marketMaker in self.stock_marketMakers.values():
            marketMaker.ordermatching_engine.match_orders()

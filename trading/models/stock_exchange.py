from typing import Dict
from .Assets.stock_market_listing import Asset
from .MarketMaker.dynamic_market_maker import DynamicMarketMaker
from .OrderEngine.order_matching_engine import OrderMatchingEngine
from .order import Order
from .MarketMaker.market_maker import MarketMaker


class StockExchange:

    def __init__(self, name):
        self.name = name
        self.asset : Dict[str,Asset] = {}
        self.stock_marketMakers : Dict[str,DynamicMarketMaker] = {}


    def submit_order(self,order : Order) :

        stock_market_listing : DynamicMarketMaker  = self.stock_marketMakers.get(order.ticker,'Key not found')

        stock_market_listing.process_order(order)

    def getMarketMaker(self,ticker_symbol) -> DynamicMarketMaker:
        return self.stock_marketMakers.get(ticker_symbol,'Key not found')

    
    def addStockMarketListing(self,ticker_symbol, company_name, last_price):

        stock_market_listing = Asset(ticker_symbol, company_name, last_price)

        order_matching_engine = OrderMatchingEngine(stock_market_listing)
        marketMaker = DynamicMarketMaker(order_matching_engine,ticker_symbol, stock_market_listing)

        self.stock_marketMakers[ticker_symbol] = marketMaker

        self.asset[stock_market_listing.ticker_symbol] = stock_market_listing

    def getStockMarketListing(self,ticker_symbol) -> Asset:
        return self.asset.get(ticker_symbol,'Key not found')

    def match_orders(self):

        for marketMaker in self.stock_marketMakers.values():
            marketMaker.ordermatching_engine.match_orders()


    def set_market_maker(self,market_maker : MarketMaker):
        self.market_maker = market_maker
    
    def set_order_matching_engine(self,order_matching_engine : OrderMatchingEngine):
        self.order_matching_engine = order_matching_engine

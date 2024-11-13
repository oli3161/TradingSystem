from typing import Dict
from .stock_market_listing import StockMarketListing
from .order import Order


class StockExchange:

    def __init__(self, name):
        self.name = name
        self.stock_market_listings : Dict[str,StockMarketListing]


    def submit_order(self,order : Order) :

        stock_market_listing : StockMarketListing  = self.stock_market_listings.get(order.ticker,'Key not found')

        stock_market_listing.submit_order(order)
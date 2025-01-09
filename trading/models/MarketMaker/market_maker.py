from abc import ABC, abstractmethod
from ..order import Order



class MarketMaker(ABC):

    
    @abstractmethod
    def process_order(self,order : Order):
        pass



class MarketMakerFactory(ABC):
    @abstractmethod
    def create_market_maker(self, order_matching_engine, ticker_symbol, stock_market_listing):
        pass
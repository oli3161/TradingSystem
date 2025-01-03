from typing import Dict
from .Assets.stock_market_listing import Asset
from .MarketMaker.dynamic_market_maker import DynamicMarketMaker,DynamictMarketMakerFactory
from .OrderEngine.order_matching_engine import SimulatedOrderMatchingEngine,SimulatedOrderMatchingEngineFactory
from .order import Order
from .constants import MODE_LIVE, MODE_SIMULATION
from .money import Money

class StockExchange:

    def __init__(self, name,mode = MODE_SIMULATION):
        self.name = name
        self.asset : Dict[str,Asset] = {}
        self.stock_marketMakers : Dict[str,DynamicMarketMaker] = {}
        self.mode = mode
        self.switch_mode(mode)


    def submit_order(self,order : Order) :

        stock_market_listing : DynamicMarketMaker  = self.stock_marketMakers.get(order.ticker,'Key not found')

        stock_market_listing.process_order(order)

    
    def addStockMarketListing(self,ticker_symbol, company_name, last_price:Money):

        # Create the stock market listing with the associated : Asset, OrderMatchingEngine and MarketMaker
        stock_market_listing = Asset(ticker_symbol, company_name, last_price)
        order_matching_engine = self.order_matching_engine_factory.create_order_matching_engine(stock_market_listing)
        marketMaker = self.market_maker_factory.create_market_maker(order_matching_engine,ticker_symbol,stock_market_listing)

        # Add the stock market listing to the stock exchange
        self.stock_marketMakers[ticker_symbol] = marketMaker
        self.asset[stock_market_listing.ticker_symbol] = stock_market_listing

        return stock_market_listing


    def match_orders(self):

        for marketMaker in self.stock_marketMakers.values():
            marketMaker.ordermatching_engine.match_orders()

    def switch_mode(self,mode):

        if mode == MODE_SIMULATION:
            self.market_maker_factory = DynamictMarketMakerFactory()
            self.order_matching_engine_factory = SimulatedOrderMatchingEngineFactory()
            self.mode = mode

        elif mode == MODE_LIVE:
            print("Live mode not supported yet")

        else:
            print("Invalid mode, please enter either 'Simulation' or 'Live'")

    
    def getMarketMaker(self,ticker_symbol) -> DynamicMarketMaker:
        return self.stock_marketMakers.get(ticker_symbol,'Key not found')
    
    def getStockMarketListing(self,ticker_symbol) -> Asset:
        return self.asset.get(ticker_symbol,'Key not found')
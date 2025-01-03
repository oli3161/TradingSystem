from .stock_exchange import StockExchange
from .stock_exchange_decorator import StockExchangeDecorator
from ..Services.yahoo_finance import YahooFinance
from ..Services.asset_price_service import AssetPriceService
from queue import Queue
from ..order import Order
from ..constants import MODE_LIVE


class LiveStockExchange(StockExchangeDecorator):

    def __init__(self,stock_exchange : StockExchange):
        stock_exchange.switch_mode(MODE_LIVE)
        super().__init__(stock_exchange)
        self.asset_price_service : AssetPriceService = YahooFinance()
        self.order_queue: Queue[Order] = Queue()
        self.ticker_set: set[str] = set()
    
    def submit_order(self, order : Order):
        
        self.order_queue.put(order)
        self.ticker_set.add(order.ticker)

        tickers = list(self.ticker_set)
        prices = self.asset_price_service.get_tickers_price(tickers)
        self.modify_assets_price(prices)

        while not self.order_queue.empty():
            order = self.order_queue.get()
            ticker_price = prices.get(order.ticker, -1)
            if ticker_price != -1:
                self.stock_exchange.submit_order(order)
            else:
                order.notify_order_cancelled("Asset not found in this market exchange")


    def modify_assets_price(self,prices:dict[str,float]):
        for ticker,price in prices.items():
            asset = self.stock_exchange.getStockMarketListing(ticker)
            if asset is None:
                self.stock_exchange.addStockMarketListing(ticker, ticker, price)
            else :
                asset.last_price = price
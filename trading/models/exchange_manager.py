from .stock_exchange import StockExchange
from .Services.yahoo_finance import YahooFinance
from .Services.asset_price_service import AssetPriceService
from queue import Queue
from . order import Order
from .constants import MODE_LIVE, MODE_SIMULATION


class ExchangeManager:

    def __init__(self,exchange : StockExchange):

        self.exchange = exchange
        self.asset_price_service : AssetPriceService = YahooFinance()
        self.order_queue: Queue[Order] = Queue()
        self.ticker_set: set[str] = set()


    # Currently handles modes: Simulation, Live (not supported yet)
    def switch_mode(self,mode):
        self.exchange.switch_mode(mode)
        if mode == MODE_LIVE:
            self.order_queue : Queue[Order] = Queue()
            self.ticker_set = set()


    def submit_order(self,order:Order):
        exchange = self.exchange
        if exchange.mode == MODE_SIMULATION:
            exchange.submit_order(order)
        elif exchange.mode == MODE_LIVE:
            self.order_queue.put(order)
            self.ticker_set.add(order.ticker)
        else:
            raise RuntimeError(f"Unsupported mode: {self.exchange.mode}")

    def match_orders(self):
        if self.exchange.mode == MODE_LIVE:
            tickers = list(self.ticker_set)
            prices = self.asset_price_service.get_tickers_price(tickers)
            self.modify_assets_price(prices)

            while not self.order_queue.empty():
                order = self.order_queue.get()
                ticker_price = prices.get(order.ticker, -1)
                if ticker_price != -1:
                    self.exchange.submit_order(order)
                else:
                    order.notify_order_cancelled("Asset not found in the market")
        self.exchange.match_orders()

    
    def modify_assets_price(self,prices:dict[str,float]):
        for ticker,price in prices.items():
            asset = self.exchange.getStockMarketListing(ticker)
            if asset is None:
                self.exchange.addStockMarketListing(ticker, ticker, price)
            else :
                asset.last_price = price
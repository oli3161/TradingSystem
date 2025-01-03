from .stock_exchange import StockExchange



class StockExchangeDecorator(StockExchange):

    def __init__(self, stock_exchange : StockExchange):
        self.stock_exchange = stock_exchange
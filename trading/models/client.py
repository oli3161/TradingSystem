from .portfolio import Portfolio
from .order import Order
from .stock_exchange import StockExchange


class Client:

    def __init__(self,id):
        self.id = id
        self.portfolio : Portfolio = Portfolio()
        


    def submit_order(self,order : Order, stock_exchange : StockExchange):

        stock_exchange.submit_order(order)


    def notify_completed_order(self,order : Order, verbose = False):
        
        self.portfolio.add_stock(order.asset.portfolio_stock)

        if verbose:
            print(order)

    def __str__(self):
        return (f"Client(id={self.id})")
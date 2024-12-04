from .order import Order
from .limit_order import LimitOrder
from .market_order import MarketOrder
from .stock_exchange import StockExchange
from .client import Client
from .assets import Assets
from .portfolio_stock import PortfolioStock
import random

class OrderFlow(Client):

    def __init__(self, id):
        Client.__init__(self, id)

    def submit_order_ntimes(self, order: Order, stock_exchange: StockExchange, n: int, min_price, max_price):
        for i in range(n):
            self.randomize_quantity(order)
            self.randomize_price(order,min_price,max_price)
            self.randomize_type(order)
            stock_exchange.submit_order(order)

    def randomize_quantity(self, order: Order):
        order.initial_quantity = random.uniform(1, 10000.0)
        

    def randomize_price(self, order: Order,upper_bound,lower_bound):
        order.price = random.uniform(upper_bound,lower_bound)  # Example price range
        

    def randomize_type(self, order: Order):
        if isinstance(order, LimitOrder):
            order.buy_order = random.choice([True, False])
        elif isinstance(order, MarketOrder):
            order.buy_order = random.choice([True, False])
        
        if order.buy_order == True:
            
            Assets(money_amount=order.price*order.initial_quantity * 10)
        else:
            
            Assets(PortfolioStock(order.ticker, order.initial_quantity))
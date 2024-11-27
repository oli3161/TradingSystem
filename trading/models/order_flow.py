

from .order import Order
from .stock_exchange import StockExchange
from .client import Client
import random

class OrderFlow(Client):

    def __init__(self,id):
        Client.__init__(self,id)

    
        

    def submit_order_ntimes(self,order : Order, stock_exchange : StockExchange,n : int):
        for i in range(n) :
            self.randomize_quantity(order)
            self.randomize_type(order)
            stock_exchange.submit_order(order)


    def randomize_quantity(self,order:Order):
        order.initial_quantity=random.uniform(0.0001, 1000000.0)
        print(order.initial_quantity)
    
    def randomize_type(self,order:Order):
        type=random.randint(1,2)
        if(type==1):
            order.order_type=True
        else :
            order.order_type=False

        print(order.order_type)
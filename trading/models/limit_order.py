# from .client import Client
from .assets import Assets
from .order import Order

class LimitOrder(Order) :

    def __init__(self,price) :
        
        Order.__init__(self)
        self.price=price


# from .client import Client
from .assets import Assets
from .order import Order

class LimitOrder(Order) :

    def __init__(self, ticker, price, quantity, client, buy_order, assets: Assets, order_status="Pending"):
        
        Order.__init__(self, ticker, price, quantity, client, buy_order, assets, order_status)
        
        self.limit_price = price


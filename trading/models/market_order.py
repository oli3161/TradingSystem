from .assets import Assets
from .order import Order

class MarketOrder(Order) :

    def __init__(self, ticker, price, quantity, client, buy_order, assets: Assets, order_status="Pending"):
        
        Order.__init__(self, ticker, price, quantity, client, buy_order, assets, order_status)

    
    def __str__(self):
        return (f"Order(ticker={self.ticker}, price={self.price}, quantity={self.initial_quantity}, remaining_quantity={self.remaining_quantity}, "
                f"order_date={self.order_date}, client={self.client}, order_type= Market Order, "
                f"order_status={self.order_status}, asset={self.asset})")
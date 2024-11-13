from .order_matching_engine import OrderMatchingEngine
from .order import Order


class MarketMaker:

    #TODO Make volume sensitivity and smallest increment dynamic
    def __init__(self,ordermatching_engine : OrderMatchingEngine):

        self.ordermatching_engine = OrderMatchingEngine()
        self.ordermatching_engine = ordermatching_engine
        self.smallest_increment = 0.01
        self.volume_sensitivity = 1000 # sensitivity to volume changes


    def process_order(self,order : Order):
        
        if order.price_type == "Market":
            self.adjust_order_price(order)

        if order.order_type == "buy":
            
            self.ordermatching_engine.add_buy_order(order)
        
        elif order.order_type == "sell":
            self.ordermatching_engine.add_sell_order(order)

        else: print(f"unimplemented {order.order_type} " + " order type.")

        


    def adjust_order_price(self,order : Order):

        buy_sell_ratio = self.ordermatching_engine.instant_buy_orders / self.ordermatching_engine.instant_sell_orders
        
        order_price_adjusted = order.price + (self.smallest_increment * buy_sell_ratio) / self.volume_sensitivity

        order.price = order_price_adjusted
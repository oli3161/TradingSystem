from .order_matching_engine import OrderMatchingEngine
from .order import Order
from .stock_market_listing import StockMarketListing


class MarketMaker:

    #TODO Make volume sensitivity and smallest increment dynamic
    def __init__(self,ordermatching_engine : OrderMatchingEngine,ticker_symbol, stock_listing : StockMarketListing):

        self.stock_listing = stock_listing
        self.ticker_symbol = ticker_symbol
        self.ordermatching_engine = ordermatching_engine
        self.ordermatching_engine = ordermatching_engine
        self.smallest_increment = 0.01
        self.volume_sensitivity = 10 # sensitivity to volume changes


    def process_order(self,order : Order):
        
        if order.price_type == "Market":
            self.adjust_order_price(order)

        if order.order_type == "buy":
            
            self.ordermatching_engine.add_buy_order(order)
        
        elif order.order_type == "sell":
            self.ordermatching_engine.add_sell_order(order)

        else: print(f"unimplemented {order.order_type} " + " order type.")

        


    def adjust_order_price(self, order: Order):

        stock_price = self.stock_listing.last_price

        if order.order_type == "buy":
            quantity = order.remaining_quantity
            self.ordermatching_engine.instant_buy_orders += quantity

            if self.ordermatching_engine.instant_sell_orders == 0:
                self.ordermatching_engine.instant_sell_orders = 1

            buy_sell_ratio = self.ordermatching_engine.instant_buy_orders / self.ordermatching_engine.instant_sell_orders

            order_price_adjusted = stock_price + (self.smallest_increment * buy_sell_ratio) / self.volume_sensitivity
            

        elif order.order_type == "sell":
            quantity = order.remaining_quantity
            self.ordermatching_engine.instant_sell_orders += quantity

            if self.ordermatching_engine.instant_buy_orders == 0:
                self.ordermatching_engine.instant_buy_orders = 1
        
            buy_sell_ratio = self.ordermatching_engine.instant_buy_orders / self.ordermatching_engine.instant_sell_orders

            order_price_adjusted = stock_price - (self.smallest_increment * buy_sell_ratio) / self.volume_sensitivity
        
        print(f"Adjusted price: {order_price_adjusted}")
        
        order.price = order_price_adjusted
        
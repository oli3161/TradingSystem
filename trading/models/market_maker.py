from .order_matching_engine import OrderMatchingEngine
from .order import Order
from .market_order import MarketOrder
from .limit_order import LimitOrder
from .stock_market_listing import StockMarketListing


class MarketMaker:

    #TODO Make volume sensitivity and smallest increment dynamic
    def __init__(self,ordermatching_engine : OrderMatchingEngine,ticker_symbol, stock_listing : StockMarketListing):

        self.stock_listing = stock_listing
        self.ticker_symbol = ticker_symbol
        self.ordermatching_engine = ordermatching_engine

        self.smallest_increment = 0.01
        self.volume_sensitivity = 10 # sensitivity to volume changes


    def process_order(self,order : Order):
        
        if isinstance(order,MarketOrder):
            self.adjust_order_price(order)

        if order.is_buy_order() == True:
            
            self.ordermatching_engine.add_buy_order(order)
        
        elif order.is_buy_order() == False:
            self.ordermatching_engine.add_sell_order(order)

        else: raise TypeError (f"unimplemented {order.is_buy_order()} " + " order type.")

        


    def adjust_order_price(self, order: Order):
        stock_price = self.stock_listing.last_price
        quantity = order.remaining_quantity

        if order.is_buy_order():

             # Ensure we avoid division by zero for both buy and sell orders
            if self.ordermatching_engine.instant_sell_orders == 0:
                self.ordermatching_engine.instant_sell_orders = 1
           
            self.ordermatching_engine.instant_buy_orders += quantity
            # Calculate buy/sell ratio
            buy_sell_ratio = self.ordermatching_engine.instant_buy_orders / self.ordermatching_engine.instant_sell_orders

            # Determine the price adjustement based on the buy/sell ratio and sensitivity
            price_adjustment = (self.smallest_increment * buy_sell_ratio) / self.volume_sensitivity
            

            # Update the bid price if the adjusted price is valid
            if price_adjustment >= self.smallest_increment:
                order_price_adjusted = stock_price + price_adjustment
                order.price = order_price_adjusted

        else:  

            # Ensure we avoid division by zero for both buy and sell orders
            if self.ordermatching_engine.instant_buy_orders == 0:
                self.ordermatching_engine.instant_buy_orders = 1
 
            self.ordermatching_engine.instant_sell_orders += quantity
            # Calculate buy/sell ratio (flipped for sell orders)
            buy_sell_ratio = self.ordermatching_engine.instant_buy_orders / self.ordermatching_engine.instant_sell_orders

            # Determine the price adjustement based on the buy/sell ratio and sensitivity
            price_adjustment = (self.smallest_increment * buy_sell_ratio) / self.volume_sensitivity
            

            # Update the ask price if the adjusted price is valid
            if price_adjustment >= self.smallest_increment:
                order_price_adjusted = stock_price - price_adjustment
                order.price = order_price_adjusted


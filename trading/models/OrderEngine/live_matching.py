from .order_engine import OrderEngine
from .order_engine import OrderEngine
from trading.models.order import Order
from trading.models.limit_order import LimitOrder
from trading.models.market_order import MarketOrder
from trading.models.Assets.stock_market_listing import Asset
from trading.models.Heaps.priority_queue import PriorityQueue
from trading.models.transaction import Transaction
from datetime import datetime
from .order_engine import OrderMatchingEngineFactory
from trading.models.money import Money

class LiveMatchingFactory(OrderMatchingEngineFactory):
    def create_order_matching_engine(self, stock_market_listing):
        return LiveMatching(stock_market_listing)

class LiveMatching(OrderEngine):


    def __init__(self,stock_listing :Asset):
        OrderEngine.__init__(self,stock_listing)


    def match_orders(self):
        
        self.match_separetly_orders('buy')
        self.match_separetly_orders('sell')

    #Side can be either 'buy' or 'sell'
    def match_separetly_orders(self,side):

        if side == 'buy':
            priority_queue : PriorityQueue = self.buy_heapq

        elif side == 'sell':
            priority_queue : PriorityQueue = self.sell_heapq

        priority_queue.initialize_matching_state()

        while not priority_queue.top_orders_verified():
            
            # Get the best buy and sell orders
            best_order = priority_queue.peek()

            if best_order is None:
                break

            if isinstance(best_order, LimitOrder):
                self.match_limit_order(best_order)

            elif isinstance(best_order, MarketOrder):
                self.match_market_order(best_order)

            else:
                # No matching possible for current best orders
                priority_queue.limit_orders_verified()

        priority_queue.initialize_matching_state()


    def match_limit_order(self,limit_order : LimitOrder):

        current_price = self.stock_listing.last_price

        if limit_order.is_buy_order() and limit_order.price >= current_price:
            self.complete_buy_transaction(limit_order,current_price)

        elif not limit_order.is_buy_order() and limit_order.price <= current_price:
            self.complete_sell_transaction(limit_order,current_price)

    def match_market_order(self,market_order : MarketOrder):

        current_price = self.stock_listing.last_price

        if market_order.is_buy_order():
            self.complete_buy_transaction(market_order,current_price)

        else:
            self.complete_sell_transaction(market_order,current_price)



    def complete_buy_transaction(self,order : Order, price : Money):

        quantity = order.remaining_quantity
        order.add_shares(order.remaining_quantity,price)

        total_cost = price * quantity
        order.remove_money(total_cost)

        

    def complete_sell_transaction(self,order : Order, price : Money):

        quantity = order.remaining_quantity
        order.remove_shares(quantity,price)

        total_cost = price * quantity
        order.add_money(total_cost)

        
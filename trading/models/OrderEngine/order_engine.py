from abc import ABC, abstractmethod
from trading.models.Heaps.priority_queue import PriorityQueue
from trading.models.transaction import Transaction
from trading.models.Assets.stock_market_listing import Asset
from trading.models.order import Order


class OrderEngine(ABC):
    """Abstract class defining the interface for order heap implementations."""

    def __init__(self,stock_listing :Asset):
        self.sell_heapq = PriorityQueue(min_heap=True)
        self.buy_heapq = PriorityQueue(min_heap=False)

        self.instant_buy_orders = 0
        self.instant_sell_orders = 0

        self.stock_listing = stock_listing
        self.transactions : list[Transaction] = []
        
    
    def add_sell_order(self, order : Order):
        
        self.sell_heapq.push(order)
        

    def add_buy_order(self, order : Order):
        
        self.buy_heapq.push(order)

    @abstractmethod
    def match_orders(self):
        """
        Matches buy and sell orders from the respective priority queues.
        """
        pass

    @abstractmethod
    def complete_transaction(self,sell_order : Order,buy_order : Order,price):
        """ """
        pass
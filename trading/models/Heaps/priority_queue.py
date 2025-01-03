import heapq
from itertools import count
from .execution_queue import ExecutionQueue
from ..limit_order import LimitOrder
from ..order import Order


class PriorityQueue(ExecutionQueue):
    def __init__(self, min_heap=True):
        """
        Initializes an OrderHeap.
        
        Args:
            min_heap (bool): If True, behaves as a min-heap (ascending order by price).
                                If False, behaves as a max-heap (descending order by price).
        """
        ExecutionQueue.__init__(self)
        self.heap : list[tuple[float,int,Order]] = []
        self.market_order_queue : list[Order]  = []
        self.counter = count()  # Unique sequence count for each item
        self.is_min_heap = min_heap
        self.limit_orders_checked = False
        self.best_orders_verified = False

    def initialize_matching_state(self):

        self.limit_orders_checked = False
        self.best_orders_verified = False

    def limit_orders_verified(self):
        self.limit_orders_checked = True


    def push(self, order: Order):
        """Adds an order to the appropriate data structure."""
        if isinstance(order, LimitOrder):
            # Use `order.price.amount` for heap sorting but retain the Money object in the order
            price = order.price.amount if self.is_min_heap else -order.price.amount
            heapq.heappush(self.heap, (price, next(self.counter), order))
        else:
            self.market_order_queue.append(order)

    
    def peek(self) -> Order:
        """Returns the best order according to the conditions without removing it."""
        if self.is_empty():
            return None
        
        self.remove_cancelled_orders()

        return self._get_best_order()

    def pop(self) -> Order:
        """Removes and returns the best order according to the conditions."""
        if self.is_empty():
            return None
    
        self.remove_cancelled_orders()

        best_order = self._get_best_order()
        if best_order in self.market_order_queue:
            self.market_order_queue.remove(best_order)
        else:
            heapq.heappop(self.heap)  # Remove the top element from the heap
        return best_order

    def _get_best_order(self):
        """Determines the best order between the heap and market order queue."""
        heap_top = self.heap[0][2] if self.heap else None  # Get order from heap (price, counter, order)
        queue_top = self.market_order_queue[0] if self.market_order_queue else None  # Get first market order

        #If limit orders have been checked, return the best market order
        if self.limit_orders_checked:
            return queue_top
        
        if not heap_top and not queue_top:
            return None

        # If only one exists, return it as the best
        if heap_top and not queue_top:
            return heap_top
        if queue_top and not heap_top:
            return queue_top

        # Compare prices
        if heap_top.price.amount != queue_top.price.amount:
            if self.is_min_heap:
                return heap_top if heap_top.price < queue_top.price else queue_top
            else:
                return heap_top if heap_top.price > queue_top.price else queue_top

        # If prices are the same, compare order_date (FIFO for queue)
        return heap_top if heap_top.order_date <= queue_top.order_date else queue_top
    
    #Returns a dictionary of the price levels in the format : {price: quantity}
    def get_order_book(self) -> dict:
        price_data = {}

        for _, _, order in self.heap:
            if order.price not in price_data:
                price_data[order.price] = 0
            price_data[order.price] += order.remaining_quantity

        return price_data
    

    def top_orders_verified(self):
        
        if not self.is_empty() and not self.best_orders_verified:
            return False
        else:
            return True

    def is_empty(self):
        """Checks if the heap is empty."""
        return len(self.heap) == 0 and len(self.market_order_queue) == 0

    def get_order_list(self):
        """Returns the heap as a list of orders."""
        return [order for _, _, order in self.heap]

    def size(self):
        """Returns the number of orders in the heap."""
        return len(self.heap)

    def __str__(self):
        return str([order for _, _, order in self.heap])
    
    def clear(self):
        """Clears the heap and market order queue."""
        self.heap.clear()
        self.market_order_queue.clear()

    def remove_cancelled_orders(self):
        """Removes cancelled orders from the top of the heap and market order queue."""
        # Remove cancelled orders from the heap
        while self.heap and (self.heap[0][2].is_cancelled() or self.heap[0][2].is_completed()):
            heapq.heappop(self.heap)

        # Remove cancelled orders from the market order queue
        while self.market_order_queue and (self.market_order_queue[0].is_cancelled() or self.market_order_queue[0].is_completed()):
            self.market_order_queue.pop(0)

import heapq
from itertools import count

from .limit_order import LimitOrder
from .order import Order
from abc import ABC, abstractmethod
from .order import Order



class AbstractExecutionQueue(ABC):
    """Abstract class defining the interface for order heap implementations."""

    def __init__(self,is_min_heap=True):
        self.is_min_heap = is_min_heap
        
    
    @abstractmethod
    def push(self, order: Order):
        """Adds an order to the heap."""
        pass

    @abstractmethod
    def pop(self) -> Order:
        """Removes and returns the highest/lowest priority order."""
        pass

    @abstractmethod
    def peek(self) -> Order:
        """Returns the highest/lowest priority order without removing it."""
        pass

    @abstractmethod
    def get_order_list(self):
        """Returns all orders in the heap as a list."""
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """Checks if the heap is empty."""
        pass



class PriorityQueue(AbstractExecutionQueue):
    def __init__(self, is_min_heap=True):
        """
        Initializes an OrderHeap.
        
        Args:
            is_min_heap (bool): If True, behaves as a min-heap (ascending order by price).
                                If False, behaves as a max-heap (descending order by price).
        """
        self.heap = []
        self.market_order_queue = []
        self.counter = count()  # Unique sequence count for each item
        self.is_min_heap = is_min_heap

    def push(self, order: Order):
        """Adds an order to the heap."""
        if isinstance(order, LimitOrder):
            self.market_order_queue.append(order)
        else:
            # Use price or -price for ordering based on heap type
            price = order.price if self.is_min_heap else -order.price
            heapq.heappush(self.heap, (price, next(self.counter), order))

    def pop(self) -> Order:
        """Removes and returns the order with the highest/lowest price."""
        if not self.is_empty():
            return heapq.heappop(self.heap)[2]
        else:
            raise IndexError("pop from an empty heap")

    def peek(self) -> Order:
        """Returns the order with the highest/lowest price without removing it."""
        if not self.is_empty():
            return self.heap[0][2]
        else:
            raise IndexError("peek from an empty heap")

    def is_empty(self):
        """Checks if the heap is empty."""
        return len(self.heap) == 0

    def get_order_list(self):
        """Returns the heap as a list of orders."""
        return [order for _, _, order in self.heap]

    def size(self):
        """Returns the number of orders in the heap."""
        return len(self.heap)

    def __str__(self):
        return str([order for _, _, order in self.heap])

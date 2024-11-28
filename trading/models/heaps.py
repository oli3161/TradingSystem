import heapq
from abc import ABC, abstractmethod
from itertools import count

from trading.models.limit_order import LimitOrder
from trading.models.order import Order
from mypy_extensions import NoReturn
from trading.models.market_order import MarketOrder
from typing import Union
from typing import List


class ExecutionQueue(ABC):
    """Abstract class defining the interface for order heap implementations."""

    def __init__(self, min_heap=True):
        self.min_heap = min_heap

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


class PriorityQueue(ExecutionQueue):
    def __init__(self, min_heap: bool = True) -> NoReturn:
        """
        Initializes an OrderHeap.

        Args:
            min_heap (bool): If True, behaves as a min-heap (ascending order by price).
                                If False, behaves as a max-heap (descending order by price).
        """
        self.heap = []
        self.market_order_queue = []
        self.counter = count()  # Unique sequence count for each item
        self.is_min_heap = min_heap

    def push(self, order: Order):
        """Adds an order to the appropriate data structure."""
        if isinstance(order, LimitOrder):
            # If it's a limit order, push it to the heap
            price = (
                order.price if self.is_min_heap else -order.price
            )  # Adjust price for heap behavior
            heapq.heappush(self.heap, (price, next(self.counter), order))
        else:
            # If it's a market order, add it to the queue
            self.market_order_queue.append(order)

    def pop(self) -> Order:
        """Removes and returns the best order according to the conditions."""
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")

        best_order = self._get_best_order()
        if best_order in self.market_order_queue:
            self.market_order_queue.remove(best_order)
        else:
            heapq.heappop(self.heap)  # Remove the top element from the heap
        return best_order

    def peek(self) -> Order:
        """Returns the best order according to the conditions without removing it."""
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")

        return self._get_best_order()

    def _get_best_order(self) -> Union[LimitOrder, MarketOrder]:
        """Determines the best order between the heap and market order queue."""
        heap_top = (
            self.heap[0][2] if self.heap else None
        )  # Get order from heap (price, counter, order)
        queue_top = (
            self.market_order_queue[0] if self.market_order_queue else None
        )  # Get first market order

        # If only one exists, return it as the best
        if heap_top and not queue_top:
            return heap_top
        if queue_top and not heap_top:
            return queue_top

        # Compare prices
        if heap_top.price != queue_top.price:
            if self.is_min_heap:
                return heap_top if heap_top.price < queue_top.price else queue_top
            else:
                return heap_top if heap_top.price > queue_top.price else queue_top

        # If prices are the same, compare order_date (FIFO for queue)
        return heap_top if heap_top.order_date <= queue_top.order_date else queue_top

    def is_empty(self) -> bool:
        """Checks if the heap is empty."""
        return len(self.heap) == 0 and len(self.market_order_queue) == 0

    def get_order_list(self) -> List:
        """Returns the heap as a list of orders."""
        return [order for _, _, order in self.heap]

    def size(self) -> int:
        """Returns the number of orders in the heap."""
        return len(self.heap)

    def __str__(self):
        return str([order for _, _, order in self.heap])

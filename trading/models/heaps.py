import heapq
from itertools import count
from .order import Order

class MinOrderHeap:
    def __init__(self):
        self.heap = []
        self.counter = count()  # Unique sequence count for each item

    def push(self, order: Order):
        """Adds an order to the heap, prioritizing by price and FIFO order for duplicate prices."""
        # Use (price, sequence_number, order) to maintain order priority
        heapq.heappush(self.heap, (order.price, next(self.counter), order))

    def pop(self)->Order:
        """Removes and returns the order with the lowest price."""
        if not self.is_empty():
            # Return only the order object
            return heapq.heappop(self.heap)[2]
        else:
            raise IndexError("pop from an empty heap")

    def peek(self) ->Order:
        """Returns the order with the lowest price without removing it."""
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


class MaxOrderHeap:
    def __init__(self):
        self.heap = []
        self.counter = count()  # Unique sequence count for each item

    def push(self, order: Order):
        """Adds an order to the heap, prioritizing by price in descending order and FIFO for duplicate prices."""
        # Use (-price, sequence_number, order) to maintain max-heap behavior
        heapq.heappush(self.heap, (-order.price, next(self.counter), order))

    def pop(self)->Order:
        """Removes and returns the order with the highest price."""
        if not self.is_empty():
            # Return only the order object
            return heapq.heappop(self.heap)[2]
        else:
            raise IndexError("pop from an empty heap")

    def peek(self) ->Order:
        """Returns the order with the highest price without removing it."""
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



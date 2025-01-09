from trading.models.order import Order
from abc import ABC, abstractmethod
from trading.models.order import Order


class ExecutionQueue(ABC):
    """Abstract class defining the interface for order heap implementations."""

    def __init__(self,min_heap=True):
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
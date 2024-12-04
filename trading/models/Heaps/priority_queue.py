import heapq
from itertools import count
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import DOUBLE_EDGE

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
        self.heap = []
        self.market_order_queue = []
        self.counter = count()  # Unique sequence count for each item
        self.is_min_heap = min_heap

    def initialize_matching_state(self):

        self.limit_orders_verified = False

    def limit_orders_is_verified(self):
        self.limit_orders_verified = True


    def push(self, order: Order):
        """Adds an order to the appropriate data structure."""
        if isinstance(order, LimitOrder):
            # If it's a limit order, push it to the heap
            price = order.price if self.is_min_heap else -order.price  # Adjust price for heap behavior
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

    def _get_best_order(self):
        """Determines the best order between the heap and market order queue."""
        heap_top = self.heap[0][2] if self.heap else None  # Get order from heap (price, counter, order)
        queue_top = self.market_order_queue[0] if self.market_order_queue else None  # Get first market order

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
    
    def vizualize(self, ticker_symbol):
        """
        Visualizes the order book and market order queue with a title and ticker symbol.
        
        Args:
            ticker_symbol (str): The symbol of the stock or asset being visualized.
        """
        # Determine the title based on whether this is a buy or sell heap
        order_type = "Sell" if self.is_min_heap else "Buy"
        print(f"==== {order_type} Order Book for {ticker_symbol} ====")
        print()

        # Visualize heap and market order queue
        self.vizualize_heap(ticker_symbol)
        self.vizualize_market_order_queue()

    def vizualize_heap(self, ticker_symbol):
        """
        Visualizes the heap with dynamic price colors (green for Buy, red for Sell),
        white for the number of orders, and the total quantity at each price level,
        using styled tables and a large title.

        Args:
            ticker_symbol (str): The symbol of the stock or asset being visualized.
        """
        console = Console()

        # Title: Buy or Sell Order Book
        order_type = "Buy" if self.is_min_heap else "Sell"
        title_text = f"[bold blue]{order_type} Order Book for {ticker_symbol}[/bold blue]"
        console.print(Panel(title_text, expand=True, style="bold cyan"))

        # Check if heap is empty
        if not self.heap:
            console.print("[bold red]Order Book (Heap) is empty.[/bold red]", style="bold")
            return

        # Aggregate data for price levels
        price_data = {}
        for _, _, order in self.heap:
            if order.price not in price_data:
                price_data[order.price] = {"count": 0, "quantity": 0}
            price_data[order.price]["count"] += 1
            price_data[order.price]["quantity"] += order.remaining_quantity

        # Determine price color based on order type
        price_color = "green bold" if self.is_min_heap else "red bold"

        # Create a table with rich styling
        table = Table(title="", box=DOUBLE_EDGE, title_style="bold green")
        table.add_column("Price Level", justify="right", style=price_color)
        table.add_column("Number of Orders", justify="right", style="white bold")
        table.add_column("Total Quantity", justify="right", style="cyan bold")

        # Add rows to the table
        for price, data in sorted(price_data.items(), reverse=not self.is_min_heap):
            table.add_row(f"{price:.2f}", str(data["count"]), str(data["quantity"]))

        # Print the table
        console.print(table)



    def vizualize_market_order_queue(self):
        """
        Visualizes the market order queue with colors and boxes.
        """
        console = Console()

        if not self.market_order_queue:
            console.print("[bold red]Market Order Queue is empty.[/bold red]", style="bold")
            return

        # Count the total number of market orders
        total_market_orders = len(self.market_order_queue)

        
        unique_prices = self.market_order_queue[0].price if self.market_order_queue else 0

        # Create a table with rich styling
        table = Table(title="Market Order Queue Summary", box=DOUBLE_EDGE, title_style="bold cyan")
        table.add_column("Metric", justify="left", style="green bold", no_wrap=True)
        table.add_column("Value", justify="left", style="bold white")

        # Add rows to the table
        table.add_row("Number of Market Orders", str(total_market_orders))
        table.add_row("Associated Prices", " ",str(unique_prices))

        # Print the table
        console.print(table)

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

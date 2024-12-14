import sys


sys.path.append('C:/Users/ogigu/OneDrive/Documents/Programming/Algo/TradingSystem/trading')  # Adjust to the actual path of the 'trading' folder

import unittest
from models import *



# Create mock clients and assets for testing
client1_assets = Assets(PortfolioStock("AAPL", 50, 150.00, 160.00), 5000)
client2_assets = Assets(PortfolioStock("AAPL", 30, 140.00, 160.00), 3000)

client1 = "Client1"
client2 = "Client2"

# Create Limit and Market Orders
limit_order1 = LimitOrder("AAPL", price=155.00, quantity=10, client=client1, buy_order=True, assets=client1_assets)

limit_order2 = LimitOrder("AAPL", price=150.00, quantity=5, client=client2, buy_order=False, assets=client2_assets)

market_order1 = MarketOrder("AAPL", price=150.01, quantity=8, client=client1, buy_order=True, assets=client1_assets)

market_order2 = MarketOrder("AAPL", price=155.01, quantity=6, client=client2, buy_order=False, assets=client2_assets)


# Example Unit Test for PriorityQueue
class TestPriorityQueue(unittest.TestCase):
    def setUp(self):
        """Initialize PriorityQueue and add orders."""
        self.min_heap_queue = PriorityQueue(min_heap=True)
        self.max_heap_queue = PriorityQueue(min_heap=False)


    def test_push_and_peek_min_heap(self):
        """Test pushing orders and retrieving the best order (min-heap)."""
        self.min_heap_queue.push(limit_order1)
        self.min_heap_queue.push(limit_order2)
        self.min_heap_queue.push(market_order1)
        self.min_heap_queue.push(market_order2)

        # Peek should return the best order based on the lowest price for min-heap
        best_order = self.min_heap_queue.peek()
        self.assertEqual(best_order.price, 150.00, "Best order should have the lowest price in a min-heap.")

    def test_push_and_peek_max_heap(self):
        """Test pushing orders and retrieving the best order (max-heap)."""
        self.max_heap_queue.push(limit_order1)
        self.max_heap_queue.push(limit_order2)
        self.max_heap_queue.push(market_order1)
        self.max_heap_queue.push(market_order2)

        # Peek should return the best order based on the highest price for max-heap
        best_order = self.max_heap_queue.peek()
        self.assertEqual(best_order.price, 155.00, "Best order should have the highest price in a max-heap.")

    def test_pop_order_min_heap(self):
        """Test popping the best order from the queue (min-heap)."""
        self.min_heap_queue.push(limit_order1)
        self.min_heap_queue.push(limit_order2)

        # Pop the best order (which should have the lowest price)
        best_order = self.min_heap_queue.pop()
        self.assertEqual(best_order.price, 150.00, "Popped order should be the lowest price order in a min-heap.")
        self.assertEqual(self.min_heap_queue.size(), 1, "Queue size should decrease after popping an order.")

    def test_pop_order_max_heap(self):
        """Test popping the best order from the queue (max-heap)."""
        self.max_heap_queue.push(limit_order1)
        self.max_heap_queue.push(limit_order2)

        # Pop the best order (which should have the highest price)
        best_order = self.max_heap_queue.pop()
        self.assertEqual(best_order.price, 155.00, "Popped order should be the highest price order in a max-heap.")
        self.assertEqual(self.max_heap_queue.size(), 1, "Queue size should decrease after popping an order.")

    def test_market_orders_priority(self):
        """Test handling of market orders in the queue (both min-heap and max-heap)."""
        # Test for min-heap
        self.min_heap_queue.push(market_order1)
        self.min_heap_queue.push(market_order2)
        # Market orders should be handled based on their arrival time
        best_order = self.min_heap_queue.peek()
        self.assertEqual(best_order, market_order1, "Market orders should be prioritized by arrival time.")

        # Test for max-heap
        self.max_heap_queue.push(market_order1)
        self.max_heap_queue.push(market_order2)
        best_order = self.max_heap_queue.peek()
        self.assertEqual(best_order, market_order1, "Market orders should be prioritized by arrival time in max-heap as well.")

    
    def test_limit_market_order_matching(self):
        """Test matching of limit and market orders in the queue."""

        limit_order1 = LimitOrder("AAPL", price=155.00, quantity=10, client=client1, buy_order=True, assets=client1_assets)
        

        market_order1 = MarketOrder("AAPL", price=150.01, quantity=8, client=client1, buy_order=True, assets=client1_assets)
        

        self.max_heap_queue.push(limit_order1)
        self.max_heap_queue.push(market_order1)

        print(self.max_heap_queue.peek())
        print(self.max_heap_queue.peek())

        

        # # Matching should occur between the limit and market orders
        # self.assertEqual(self.min_heap_queue.size(), 1, "Matching should remove orders from the queue.")
        # self.assertEqual(self.max_heap_queue.size(), 1, "Matching should remove orders from the queue.")

if __name__ == "__main__":
    unittest.main()


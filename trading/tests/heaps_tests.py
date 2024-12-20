import sys

sys.path.append('C:/Users/ogigu/OneDrive/Documents/Programming/Algo/TradingSystem/trading')  # Adjust to the actual path of the 'trading' folder

from models import *

import pytest

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

@pytest.fixture
def min_heap_queue():
    """Fixture for a min-heap PriorityQueue."""
    return PriorityQueue(min_heap=True)

@pytest.fixture
def max_heap_queue():
    """Fixture for a max-heap PriorityQueue."""
    return PriorityQueue(min_heap=False)

def test_push_and_peek_min_heap(min_heap_queue):
    """Test pushing orders and retrieving the best order (min-heap)."""
    min_heap_queue.push(limit_order1)
    min_heap_queue.push(limit_order2)
    min_heap_queue.push(market_order1)
    min_heap_queue.push(market_order2)

    # Peek should return the best order based on the lowest price for min-heap
    best_order = min_heap_queue.peek()
    assert best_order.price == 150.00, "Best order should have the lowest price in a min-heap."

def test_push_and_peek_max_heap(max_heap_queue):
    """Test pushing orders and retrieving the best order (max-heap)."""
    max_heap_queue.push(limit_order1)
    max_heap_queue.push(limit_order2)
    max_heap_queue.push(market_order1)
    max_heap_queue.push(market_order2)

    # Peek should return the best order based on the highest price for max-heap
    best_order = max_heap_queue.peek()
    assert best_order.price == 155.00, "Best order should have the highest price in a max-heap."

def test_pop_order_min_heap(min_heap_queue):
    """Test popping the best order from the queue (min-heap)."""
    min_heap_queue.push(limit_order1)
    min_heap_queue.push(limit_order2)

    # Pop the best order (which should have the lowest price)
    best_order = min_heap_queue.pop()
    assert best_order.price == 150.00, "Popped order should be the lowest price order in a min-heap."
    assert min_heap_queue.size() == 1, "Queue size should decrease after popping an order."

def test_pop_order_max_heap(max_heap_queue):
    """Test popping the best order from the queue (max-heap)."""
    max_heap_queue.push(limit_order1)
    max_heap_queue.push(limit_order2)

    # Pop the best order (which should have the highest price)
    best_order = max_heap_queue.pop()
    assert best_order.price == 155.00, "Popped order should be the highest price order in a max-heap."
    assert max_heap_queue.size() == 1, "Queue size should decrease after popping an order."

def test_market_orders_priority(min_heap_queue, max_heap_queue):
    """Test handling of market orders in the queue (both min-heap and max-heap)."""
    # Test for min-heap
    min_heap_queue.push(market_order1)
    min_heap_queue.push(market_order2)
    # Market orders should be handled based on their arrival time
    best_order = min_heap_queue.peek()
    assert best_order == market_order1, "Market orders should be prioritized by arrival time."

    # Test for max-heap
    max_heap_queue.push(market_order1)
    max_heap_queue.push(market_order2)
    best_order = max_heap_queue.peek()
    assert best_order == market_order1, "Market orders should be prioritized by arrival time in max-heap as well."

def test_limit_market_order_matching(max_heap_queue):
    """Test matching of limit and market orders in the queue."""
    limit_order = LimitOrder("AAPL", price=155.00, quantity=10, client=client1, buy_order=True, assets=client1_assets)
    market_order = MarketOrder("AAPL", price=150.01, quantity=8, client=client1, buy_order=True, assets=client1_assets)

    max_heap_queue.push(limit_order)
    max_heap_queue.push(market_order)


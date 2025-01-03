from ...models import *
import pytest
import time

# Create mock clients and assets for testing
client1_assets = Assets(PortfolioStock("AAPL", 50, 150.00, 160.00), Money(5000))
client2_assets = Assets(PortfolioStock("AAPL", 30, 140.00, 160.00), Money(3000))

client1 = "Client1"
client2 = "Client2"

# Create Limit and Market Orders
buy_limit_order = LimitOrder("AAPL", price=Money(155.00), quantity=10, client=client1, buy_order=True, assets=client1_assets)
sell_limit_order = LimitOrder("AAPL", price=Money(150.00), quantity=5, client=client2, buy_order=False, assets=client2_assets)
buy_market_order = MarketOrder("AAPL", price=Money(150.01), quantity=8, client=client1, buy_order=True, assets=client1_assets)
sell_market_order = MarketOrder("AAPL", price=Money(155.01), quantity=6, client=client2, buy_order=False, assets=client2_assets)

@pytest.fixture
def min_heap_queue():
    """Fixture for a min-heap PriorityQueue. Used for sell orders."""
    return PriorityQueue(min_heap=True)

@pytest.fixture
def max_heap_queue():
    """Fixture for a max-heap PriorityQueue. Used for buy orders."""
    return PriorityQueue(min_heap=False)

def test_push_and_peek_min_heap(min_heap_queue):
    """Test pushing orders and retrieving the best order (min-heap)."""
    min_heap_queue.push(buy_limit_order)
    min_heap_queue.push(sell_limit_order)
    min_heap_queue.push(buy_market_order)
    min_heap_queue.push(sell_market_order)

    # Peek should return the best order based on the lowest price for min-heap
    best_order = min_heap_queue.peek()
    assert best_order.price == 150.00, "Best order should have the lowest price in a min-heap."

def test_push_and_peek_max_heap(max_heap_queue):
    """Test pushing orders and retrieving the best order (max-heap)."""
    max_heap_queue.push(buy_limit_order)
    max_heap_queue.push(sell_limit_order)
    max_heap_queue.push(buy_market_order)
    max_heap_queue.push(sell_market_order)

    # Peek should return the best order based on the highest price for max-heap
    best_order = max_heap_queue.peek()
    assert best_order.price == 155.00, "Best order should have the highest price in a max-heap."

def test_pop_order_min_heap(min_heap_queue):
    """Test popping the best order from the queue (min-heap)."""
    min_heap_queue.push(buy_limit_order)
    min_heap_queue.push(sell_limit_order)

    # Pop the best order (which should have the lowest price)
    best_order = min_heap_queue.pop()
    assert best_order.price == 150.00, "Popped order should be the lowest price order in a min-heap."
    assert min_heap_queue.size() == 1, "Queue size should decrease after popping an order."

def test_pop_order_max_heap(max_heap_queue):
    """Test popping the best order from the queue (max-heap)."""
    max_heap_queue.push(buy_limit_order)
    max_heap_queue.push(sell_limit_order)

    # Pop the best order (which should have the highest price)
    best_order = max_heap_queue.pop()
    assert best_order.price == 155.00, "Popped order should be the highest price order in a max-heap."
    assert max_heap_queue.size() == 1, "Queue size should decrease after popping an order."

def test_market_orders_priority(min_heap_queue, max_heap_queue):
    """Test handling of market orders in the queue (both min-heap and max-heap)."""
    # Test for min-heap
    min_heap_queue.push(buy_market_order)
    min_heap_queue.push(sell_market_order)
    # Market orders should be handled based on their arrival time
    best_order = min_heap_queue.peek()
    assert best_order == buy_market_order, "Market orders should be prioritized by arrival time."

    # Test for max-heap
    max_heap_queue.push(buy_market_order)
    max_heap_queue.push(sell_market_order)
    best_order = max_heap_queue.peek()
    assert best_order == buy_market_order, "Market orders should be prioritized by arrival time in max-heap as well."

def test_limit_market_order_matching(max_heap_queue):
    """Test matching of limit and market orders in the queue."""
    limit_order = LimitOrder("AAPL", price=155.00, quantity=10, client=client1, buy_order=True, assets=client1_assets)
    market_order = MarketOrder("AAPL", price=150.01, quantity=8, client=client1, buy_order=True, assets=client1_assets)

    max_heap_queue.push(limit_order)
    max_heap_queue.push(market_order)

def test_order_submitted(max_heap_queue: PriorityQueue):

    buy_market_order2 = MarketOrder("AAPL", price=155.00, quantity=8, client=client1, buy_order=True, assets=client1_assets)
    max_heap_queue.push(buy_market_order2)

    time.sleep(0.01)
    buy_limit_order2 = LimitOrder("AAPL", price=155.00, quantity=10, client=client1, buy_order=True, assets=client1_assets)
    max_heap_queue.push(buy_limit_order2)

    assert max_heap_queue.pop() == buy_market_order2, "Time priority should be respected for orders with the same price."

    max_heap_queue.clear()
    assert max_heap_queue.size() == 0, "Queue should be empty after clearing."
    
    #Test the opposite
    buy_limit_order2 = LimitOrder("AAPL", price=155.00, quantity=10, client=client1, buy_order=True, assets=client1_assets)
    max_heap_queue.push(buy_limit_order2)

    time.sleep(0.01)
    buy_market_order2 = MarketOrder("AAPL", price=155.00, quantity=8, client=client1, buy_order=True, assets=client1_assets)
    max_heap_queue.push(buy_market_order2)
    

    assert max_heap_queue.pop() == buy_limit_order2, "Time priority should be respected for orders with the same price."


def test_cancelled_orders(max_heap_queue: PriorityQueue):
    """Test handling of cancelled orders in the queue."""
    limit_order = LimitOrder("AAPL", price=155.00, quantity=10, client=client1, buy_order=True, assets=client1_assets)
    market_order = MarketOrder("AAPL", price=150.01, quantity=8, client=client1, buy_order=True, assets=client1_assets)

    max_heap_queue.push(limit_order)
    max_heap_queue.push(market_order)

    assert max_heap_queue.size() + len(max_heap_queue.market_order_queue) == 2, "Queue should contain both orders."

    # Cancel the limit order
    limit_order.notify_order_cancelled("hey")
    best_order = max_heap_queue.peek()
    assert best_order == market_order, "Cancelled orders should be skipped when peeking."

    # Cancel the market order
    market_order.notify_order_cancelled("hey")
    best_order = max_heap_queue.peek()
    assert best_order is None, "Queue should be empty after cancelling all orders."
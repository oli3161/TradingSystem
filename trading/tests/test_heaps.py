import pytest

from trading.models.assets import Assets
from trading.models.heaps import PriorityQueue
from trading.models.limit_order import LimitOrder
from trading.models.market_order import MarketOrder
from trading.models.portfolio_stock import PortfolioStock
from typing import Tuple
from mypy_extensions import NoReturn


# Create mock clients and assets for testing
@pytest.fixture
def mock_data() -> Tuple[LimitOrder, LimitOrder, MarketOrder, MarketOrder]:
    client1_assets = Assets(PortfolioStock("AAPL", 50, 150.00, 160.00), 5000)
    client2_assets = Assets(PortfolioStock("AAPL", 30, 140.00, 160.00), 3000)

    client1 = "Client1"
    client2 = "Client2"

    limit_order1 = LimitOrder(
        "AAPL",
        price=155.00,
        quantity=10,
        client=client1,
        buy_order=True,
        assets=client1_assets,
    )
    limit_order2 = LimitOrder(
        "AAPL",
        price=150.00,
        quantity=5,
        client=client2,
        buy_order=False,
        assets=client2_assets,
    )
    market_order1 = MarketOrder(
        "AAPL",
        price=150.01,
        quantity=8,
        client=client1,
        buy_order=True,
        assets=client1_assets,
    )
    market_order2 = MarketOrder(
        "AAPL",
        price=155.01,
        quantity=6,
        client=client2,
        buy_order=False,
        assets=client2_assets,
    )

    return limit_order1, limit_order2, market_order1, market_order2


@pytest.fixture
def priority_queues() -> Tuple[PriorityQueue, PriorityQueue]:
    min_heap_queue = PriorityQueue(min_heap=True)
    max_heap_queue = PriorityQueue(min_heap=False)
    return min_heap_queue, max_heap_queue


def test_push_and_peek_min_heap(priority_queues: Tuple[PriorityQueue, PriorityQueue], mock_data: Tuple[LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    """Test pushing orders and retrieving the best order (min-heap)."""
    min_heap_queue, _ = priority_queues
    limit_order1, limit_order2, market_order1, market_order2 = mock_data

    min_heap_queue.push(limit_order1)
    min_heap_queue.push(limit_order2)
    min_heap_queue.push(market_order1)
    min_heap_queue.push(market_order2)

    # Peek should return the best order based on the lowest price for min-heap
    best_order = min_heap_queue.peek()
    assert (
        best_order.price == 150.00
    ), "Best order should have the lowest price in a min-heap."


def test_push_and_peek_max_heap(priority_queues: Tuple[PriorityQueue, PriorityQueue], mock_data: Tuple[LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    """Test pushing orders and retrieving the best order (max-heap)."""
    _, max_heap_queue = priority_queues
    limit_order1, limit_order2, market_order1, market_order2 = mock_data

    max_heap_queue.push(limit_order1)
    max_heap_queue.push(limit_order2)
    max_heap_queue.push(market_order1)
    max_heap_queue.push(market_order2)

    # Peek should return the best order based on the highest price for max-heap
    best_order = max_heap_queue.peek()
    assert (
        best_order.price == 155.00
    ), "Best order should have the highest price in a max-heap."


def test_pop_order_min_heap(priority_queues: Tuple[PriorityQueue, PriorityQueue], mock_data: Tuple[LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    """Test popping the best order from the queue (min-heap)."""
    min_heap_queue, _ = priority_queues
    limit_order1, limit_order2, _, _ = mock_data

    min_heap_queue.push(limit_order1)
    min_heap_queue.push(limit_order2)

    # Pop the best order (which should have the lowest price)
    best_order = min_heap_queue.pop()
    assert (
        best_order.price == 150.00
    ), "Popped order should be the lowest price order in a min-heap."
    assert (
        min_heap_queue.size() == 1
    ), "Queue size should decrease after popping an order."


def test_pop_order_max_heap(priority_queues: Tuple[PriorityQueue, PriorityQueue], mock_data: Tuple[LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    """Test popping the best order from the queue (max-heap)."""
    _, max_heap_queue = priority_queues
    limit_order1, limit_order2, _, _ = mock_data

    max_heap_queue.push(limit_order1)
    max_heap_queue.push(limit_order2)

    # Pop the best order (which should have the highest price)
    best_order = max_heap_queue.pop()
    assert (
        best_order.price == 155.00
    ), "Popped order should be the highest price order in a max-heap."
    assert (
        max_heap_queue.size() == 1
    ), "Queue size should decrease after popping an order."


def test_market_orders_priority(priority_queues: Tuple[PriorityQueue, PriorityQueue], mock_data: Tuple[LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    """Test handling of market orders in the queue (both min-heap and max-heap)."""
    min_heap_queue, max_heap_queue = priority_queues
    _, _, market_order1, market_order2 = mock_data

    # Test for min-heap
    min_heap_queue.push(market_order1)
    min_heap_queue.push(market_order2)
    # Market orders should be handled based on their arrival time
    best_order = min_heap_queue.peek()
    assert (
        best_order == market_order1
    ), "Market orders should be prioritized by arrival time."

    # Test for max-heap
    max_heap_queue.push(market_order1)
    max_heap_queue.push(market_order2)
    best_order = max_heap_queue.peek()
    assert (
        best_order == market_order1
    ), "Market orders should be prioritized by arrival time in max-heap as well."

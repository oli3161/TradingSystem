import pytest
from datetime import datetime
from ..models import *

@pytest.fixture
def setup_engine():
    """
    Fixture to set up the OrderMatchingEngine with required dependencies.
    """
    stock_listing = Asset("AAPL", "Apple", 101.0)  # Example stock listing
    engine = OrderMatchingEngine(stock_listing)
    return engine

@pytest.fixture
def create_order():
    """
    Helper to create an order with mock data.
    """
    def _create_order(ticker, price, quantity, client_name, buy_order=True):
        client = Client(client_name)
        if buy_order:
            
            assets = Assets(money_amount=10000)  # Mock assets with 10k cash
        else :
            assets = Assets(PortfolioStock(ticker,quantity))
        return Order(ticker, price, quantity, client, buy_order, assets)
    return _create_order

def test_add_buy_order(setup_engine, create_order):
    """
    Test adding a buy order.
    """
    engine = setup_engine
    buy_order = create_order("AAPL", 102.0, 10, "Alice", True)
    engine.add_buy_order(buy_order)
    assert engine.buy_heapq.peek() == buy_order, "Buy order should be added to the buy heap"

def test_add_sell_order(setup_engine, create_order):
    """
    Test adding a sell order.
    """
    engine = setup_engine
    sell_order = create_order("AAPL", 99.0, 5, "Bob", False)
    engine.add_sell_order(sell_order)
    assert engine.sell_heapq.peek() == sell_order, "Sell order should be added to the sell heap"

def test_match_market_orders(setup_engine, create_order):
    """
    Test matching two market orders.
    """
    engine = setup_engine
    buy_order = create_order("AAPL", 105.0, 10, "Alice", True)
    sell_order = create_order("AAPL", 95.0, 10, "Bob", False)

    engine.add_buy_order(buy_order)
    engine.add_sell_order(sell_order)

    engine.match_market_orders(sell_order, buy_order)

    # Verify adjusted prices
    assert buy_order.price > sell_order.price, "Buy price should be greater after spread adjustment"

    # Verify transaction recording
    assert len(engine.transactions) == 1, "One transaction should be recorded"



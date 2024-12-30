import logging

logging.basicConfig(level=logging.INFO)

import pytest
from trading.models import *

@pytest.fixture
def setup_environment():
    """Fixture to set up the testing environment."""
    stock_exchange = StockExchange("Quebek")
    stock_exchange.addStockMarketListing("AAPL", "Apple Inc", 150.0)
    market_maker = stock_exchange.getMarketMaker("AAPL")
    order_matching_engine = market_maker.ordermatching_engine


    return {
        "stock_exchange": stock_exchange,
        "market_maker": market_maker,
        "order_matching_engine": order_matching_engine,
    }

@pytest.fixture
def setup_limit_orders():
    """Fixture to set up limit orders for testing."""
    client1_assets = Assets( 5000)
    client2_assets = Assets(PortfolioStock("AAPL", 30, 140.00, 160.00))

    client1 = "Client1"
    client2 = "Client2"

    limit_buy_order = LimitOrder("AAPL", price=155.00, quantity=10, client=client1, buy_order=True, assets=client1_assets)
    limit_sell_order = LimitOrder("AAPL", price=150.00, quantity=5, client=client2, buy_order=False, assets=client2_assets)

    return {
        "limit_buy_order": limit_buy_order,
        "limit_sell_order": limit_sell_order,
    } 

@pytest.fixture
def setup_market_orders():
    """Fixture to set up limit orders for testing."""
    client1_assets = Assets( 5000)
    client2_assets = Assets(PortfolioStock("AAPL", 30, 140.00, 160.00))

    client1 = "Client1"
    client2 = "Client2"

    market_buy_order = MarketOrder("AAPL", price=155.00, quantity=10, client=client1, buy_order=True, assets=client1_assets)
    market_sell_order = MarketOrder("AAPL", price=150.00, quantity=5, client=client2, buy_order=False, assets=client2_assets)

    return {
        "market_buy_order": market_buy_order,
        "market_sell_order": market_sell_order,
    } 


def test_limit_order(setup_environment,setup_limit_orders):
    """Test the processing of limit orders."""
    stock_exchange = setup_environment["stock_exchange"]
    market_maker = setup_environment["market_maker"]
    order_matching_engine : SimulatedOrderMatchingEngine = setup_environment["order_matching_engine"]
    limit_buy_order = setup_limit_orders["limit_buy_order"]
    limit_sell_order = setup_limit_orders["limit_sell_order"]

    market_maker.process_order(limit_buy_order)
    market_maker.process_order(limit_sell_order)

    order_matching_engine.buy_heapq.size()

    assert order_matching_engine.buy_heapq.size() == 1, "Buy order should be added to the buy orders list."
    assert order_matching_engine.sell_heapq.size() == 1, "Sell order should be added to the sell orders list."
    assert order_matching_engine.buy_heapq.peek().price == 155.00, "Buy order should be at the top of the buy orders list."
    assert order_matching_engine.sell_heapq.peek().price == 150.00, "Sell order should be at the top of the sell orders list."


def test_market_buy_order01(setup_environment,setup_market_orders):
    """Test the processing of market orders."""
    stock_exchange = setup_environment["stock_exchange"]
    market_maker : DynamicMarketMaker = setup_environment["market_maker"]
    order_matching_engine : SimulatedOrderMatchingEngine = setup_environment["order_matching_engine"]
    market_buy_order = setup_market_orders["market_buy_order"]
    market_sell_order = setup_market_orders["market_sell_order"]
    market_maker.volume_sensitivity = 10000

    market_maker.process_order(market_buy_order)
    market_maker.process_order(market_sell_order)


    assert stock_exchange.getStockMarketListing("AAPL").bid_price == 150.00, "Bid price should be updated based on the market order."
    assert stock_exchange.getStockMarketListing("AAPL").ask_price == 150.00, "Ask price should be updated based on the market order."


def test_market_buy_order02(setup_environment,setup_market_orders):
    """Test the processing of market orders."""
    stock_exchange = setup_environment["stock_exchange"]
    market_maker : DynamicMarketMaker = setup_environment["market_maker"]
    order_matching_engine : SimulatedOrderMatchingEngine = setup_environment["order_matching_engine"]
    market_buy_order = setup_market_orders["market_buy_order"]
    market_sell_order = setup_market_orders["market_sell_order"]
    market_maker.volume_sensitivity = 10000

    market_maker.process_order(market_buy_order)
    market_maker.process_order(market_sell_order)


    assert stock_exchange.getStockMarketListing("AAPL").bid_price == 150.00, "Bid price should be updated based on the market order."
    
    


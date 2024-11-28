import pytest

from trading.models.assets import Assets
from trading.models.client import Client
from trading.models.limit_order import LimitOrder
from trading.models.market_order import MarketOrder
from trading.models.order_matching_engine import OrderMatchingEngine
from trading.models.portfolio_stock import PortfolioStock
from trading.models.stock_market_listing import StockMarketListing
from typing import Tuple
from mypy_extensions import NoReturn


@pytest.fixture
def setup_engine() -> Tuple[OrderMatchingEngine, StockMarketListing, LimitOrder, LimitOrder, MarketOrder, MarketOrder]:
    """Fixture to set up the order matching engine and mock data."""
    # Create a mock stock listing
    stock_listing = StockMarketListing("AAPL", 150.00, 155.00)  # Initial bid and ask
    engine = OrderMatchingEngine(stock_listing)

    # Create mock clients and assets
    client1_assets = Assets(PortfolioStock("AAPL", 50, 150.00, 160.00), 5000)
    client2_assets = Assets(PortfolioStock("AAPL", 30, 140.00, 160.00), 3000)

    limit_order_buy = LimitOrder(
        "AAPL",
        price=150.00,
        quantity=10,
        client=Client(1),
        buy_order=True,
        assets=client1_assets,
    )
    limit_order_sell = LimitOrder(
        "AAPL",
        price=155.00,
        quantity=5,
        client=Client(2),
        buy_order=False,
        assets=client2_assets,
    )
    market_order_buy = MarketOrder(
        "AAPL",
        price=155.00,
        quantity=5,
        client=Client(1),
        buy_order=True,
        assets=client1_assets,
    )
    market_order_sell = MarketOrder(
        "AAPL",
        price=150.00,
        quantity=5,
        client=Client(2),
        buy_order=False,
        assets=client2_assets,
    )

    return (
        engine,
        stock_listing,
        limit_order_buy,
        limit_order_sell,
        market_order_buy,
        market_order_sell,
    )


def test_add_buy_order(setup_engine: Tuple[OrderMatchingEngine, StockMarketListing, LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    engine, _, limit_order_buy, _, _, _ = setup_engine
    engine.add_buy_order(limit_order_buy)
    assert engine.buy_heapq.peek().price == 150.00


def test_add_sell_order(setup_engine: Tuple[OrderMatchingEngine, StockMarketListing, LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    engine, _, _, limit_order_sell, _, _ = setup_engine
    engine.add_sell_order(limit_order_sell)
    assert engine.sell_heapq.peek().price == 155.00


def test_order_matching_limit_to_limit(setup_engine: Tuple[OrderMatchingEngine, StockMarketListing, LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    engine, _, limit_order_buy, limit_order_sell, _, _ = setup_engine
    engine.add_buy_order(limit_order_buy)
    engine.add_sell_order(limit_order_sell)

    engine.match_orders()
    assert len(engine.transactions) == 1
    transaction = engine.transactions[0]
    assert transaction.price == 155.00  # Transaction should be at the ask price


def test_order_matching_limit_to_market(setup_engine: Tuple[OrderMatchingEngine, StockMarketListing, LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    engine, _, limit_order_buy, _, _, market_order_sell = setup_engine
    engine.add_buy_order(limit_order_buy)
    engine.add_sell_order(market_order_sell)

    engine.match_orders()
    assert len(engine.transactions) == 1
    transaction = engine.transactions[0]
    assert (
        transaction.price == 150.00
    )  # Transaction price should be the limit order price


def test_order_matching_market_to_limit(setup_engine: Tuple[OrderMatchingEngine, StockMarketListing, LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    engine, _, _, limit_order_sell, market_order_buy, _ = setup_engine
    engine.add_buy_order(market_order_buy)
    engine.add_sell_order(limit_order_sell)

    engine.match_orders()
    assert len(engine.transactions) == 1
    transaction = engine.transactions[0]
    assert (
        transaction.price == 155.00
    )  # Transaction price should be the limit order price


def test_order_matching_market_to_market(setup_engine: Tuple[OrderMatchingEngine, StockMarketListing, LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    engine, _, _, _, market_order_buy, market_order_sell = setup_engine
    engine.add_buy_order(market_order_buy)
    engine.add_sell_order(market_order_sell)

    engine.match_orders()
    assert len(engine.transactions) == 1
    transaction = engine.transactions[0]
    assert transaction.price == 152.50  # Midprice between the two market orders


def test_partial_fill(setup_engine: Tuple[OrderMatchingEngine, StockMarketListing, LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    engine, _, limit_order_buy, limit_order_sell, _, _ = setup_engine

    limit_order_buy.quantity = 5  # Adjust the buy order quantity
    engine.add_buy_order(limit_order_buy)
    engine.add_sell_order(limit_order_sell)

    engine.match_orders()
    assert len(engine.transactions) == 1
    transaction = engine.transactions[0]
    assert transaction.quantity == 5  # Only 5 shares should have been traded


def test_no_match(setup_engine: Tuple[OrderMatchingEngine, StockMarketListing, LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    engine, _, limit_order_buy, limit_order_sell, _, _ = setup_engine
    engine.add_buy_order(limit_order_buy)
    engine.add_sell_order(limit_order_sell)

    engine.match_orders()
    assert len(engine.transactions) == 0


def test_transaction_update(setup_engine: Tuple[OrderMatchingEngine, StockMarketListing, LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    engine, stock_listing, limit_order_buy, limit_order_sell, _, _ = setup_engine

    engine.add_buy_order(limit_order_buy)
    engine.add_sell_order(limit_order_sell)
    engine.match_orders()

    assert stock_listing.last_price == 155.00  # Verify that the stock price updates


def test_spread_in_market_orders(setup_engine: Tuple[OrderMatchingEngine, StockMarketListing, LimitOrder, LimitOrder, MarketOrder, MarketOrder]) -> NoReturn:
    engine, _, _, _, market_order_buy, market_order_sell = setup_engine
    engine.add_buy_order(market_order_buy)
    engine.add_sell_order(market_order_sell)

    engine.match_orders()
    assert len(engine.transactions) == 1
    transaction = engine.transactions[0]
    assert transaction.price == 152.50  # Midprice between market orders

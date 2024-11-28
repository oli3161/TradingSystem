import pytest

from trading.models.client import Client
from trading.models.portfolio_stock import PortfolioStock
from trading.models.assets import Assets
from trading.models.stock_exchange import StockExchange
from trading.models.market_maker import MarketMaker
from trading.models.order import Order

@pytest.fixture
def setup_market():
    stock_exchange = StockExchange("Quebek")

    stock_exchange.addStockMarketListing("AAPL", "Apple Inc", 150.0)
    market_maker = stock_exchange.getMarketMaker("AAPL")
    order_matching_engine = market_maker.ordermatching_engine

    client_buyer = Client("JoeBlow")
    buyer_asset = Assets(money_amount=1000)

    client_seller = Client("PoorBobby")
    seller_stock = PortfolioStock("AAPL", 10, 120.0, 150)
    seller_asset = Assets(seller_stock, 0)

    return stock_exchange, market_maker, order_matching_engine, client_buyer, buyer_asset, client_seller, seller_asset

def test_add_buy_order(setup_market):
    stock_exchange, market_maker, _, _, _, _, _ = setup_market

    order = Order(
        "AAPL",
        100,
        400,
        "2021-01-01",
        Client("ClientName"),
        True,
        Assets(PortfolioStock("AAPL", 10, 150.0, 120), 1000)
    )
    stock_exchange.submit_order(order)

    # Assert the order is in the buy heap
    assert order in market_maker.ordermatching_engine.buy_heapq.get_order_list()

def test_match_orders(setup_market):
    stock_exchange, _, order_matching_engine, _, _, _, _ = setup_market

    buy_order = Order(
        "AAPL",
        100,
        5,
        "2021-01-01",
        Client("ClientName"),
        True,
        Assets(PortfolioStock("AAPL", 10, 150.0, 120), 1000)
    )
    stock_exchange.submit_order(buy_order)

    sell_order = Order(
        "AAPL",
        100,
        5,
        "2021-01-01",
        Client("ClientName"),
        False,
        Assets(PortfolioStock("AAPL", 10, 150.0, 120), 1000)
    )
    stock_exchange.submit_order(sell_order)

    order_matching_engine.match_orders()

    # Assert buy and sell heaps are empty after matching
    assert order_matching_engine.buy_heapq.get_order_list() == []
    assert order_matching_engine.sell_heapq.get_order_list() == []

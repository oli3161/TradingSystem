import pytest

from trading.models.client import Client
from trading.models.portfolio_stock import PortfolioStock
from trading.models.order import Order
from trading.models.stock_exchange import StockExchange
from trading.models.assets import Assets
from trading.models.order_flow import OrderFlow

@pytest.fixture
def setup_environment():
    client = Client("TestClients")
    portfolio_stock = PortfolioStock("AAPL", 10, 150.0, 120)
    asset = Assets(portfolio_stock, 0)
    order = Order("AAPL", 150.0, 10, "2021-01-01", client, "Sell", asset)
    stock_exchange = StockExchange("TestStockExchange")
    stock_exchange.addStockMarketListing("AAPL", "Apple Inc", 150.0)
    engine = stock_exchange.getMarketMaker("AAPL").ordermatching_engine
    return client, portfolio_stock, order, stock_exchange, engine

def test_client_initialization(setup_environment):
    client, _, _, _, _ = setup_environment
    assert client.id == "TestClients"
    assert len(client.portfolio.stocks) == 0

def test_add_stock_to_portfolio(setup_environment):
    client, portfolio_stock, _, _, _ = setup_environment
    client.portfolio.add_stock(portfolio_stock)
    assert len(client.portfolio.stocks) == 1
    assert client.portfolio.stocks[0].ticker_symbol == "AAPL"

def test_order_flow(setup_environment):
    _, _, order, stock_exchange, engine = setup_environment
    order_flow = OrderFlow("TestOrderFlow")
    order_flow.submit_order_ntimes(order, stock_exchange, 10)
    total_orders = len(engine.buy_heapq.get_order_list()) + len(engine.sell_heapq.get_order_list())
    assert total_orders == 10

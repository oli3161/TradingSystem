import sys

from ETS.AlgoETS.Simulateur.TradingSystem.TradingSystem.trading.models.order_flow import OrderFlow
sys.path.append('C:/Users/ogigu/OneDrive/Documents/Ecole/Algo/TradingSystem/trading')  # Adjust to the actual path of the 'trading' folder

import unittest
from unittest.mock import Mock
from models import *


class TestClient(unittest.TestCase):

    def setUpStockExchange(self):

        self.stock_exchange = StockExchange("TestStockExchange")
        stock_listing = StockMarketListing("AAPL", "Apple Inc",)

        
        
    def setUp(self):
        self.client = Client("TestClient")
        self.portfolio_stock = PortfolioStock("AAPL", 10, 150.0,120)
        asset = Assets(self.portfolio_stock,0)
        self.order = Order("AAPL", 150.0, 10, "2021-01-01", self.client,"Sell",asset)

    def test_client_initialization(self):
        self.assertEqual(self.client.name, "TestClient")
        self.assertEqual(len(self.client.portfolio.stocks), 0)

    def test_add_stock_to_portfolio(self):
        self.client.portfolio.add_stock(self.portfolio_stock)
        self.assertEqual(len(self.client.portfolio.stocks), 1)
        self.assertEqual(self.client.portfolio.stocks[0].ticker, "AAPL")

    def test_submit_order(self):
        market_maker_mock = Mock()
        self.client.market_maker = market_maker_mock
        self.client.submit_order(self.order,self.stock_exchange)
        market_maker_mock.process_order.assert_called_once_with(self.order)

    def test_order_flow(self):
        order_flow=OrderFlow(self.client)
        order_flow.submit_order_ntimes(self.order,self.stock_exchange,10)
        



if __name__ == '__main__':
    unittest.main()




import sys





sys.path.append('C:/A/ETS/AlgoETS/Simulateur/TradingSystem/TradingSystem/trading')  # Adjust to the actual path of the 'trading' folder

import unittest
from unittest.mock import Mock
from models import *


class TestClient(unittest.TestCase):

    # def setUpStockExchange(self):

        
        
        
    def setUp(self):
        self.client = Client("TestClients")
        self.portfolio_stock = PortfolioStock("AAPL", 10, 150.0,120)
        asset = Assets(self.portfolio_stock,0)
        self.order = Order("AAPL", 150.0, 10, "2021-01-01", self.client,"Sell",asset)
        self.stock_exchange = StockExchange("TestStockExchange")
        self.stock_exchange.addStockMarketListing("AAPL", "Apple Inc", 150.0)
        
        self.engine = self.stock_exchange.getMarketMaker("AAPL").ordermatching_engine

    def test_client_initialization(self):
        self.assertEqual(self.client.id, "TestClients")
        self.assertEqual(len(self.client.portfolio.stocks), 0)

    def test_add_stock_to_portfolio(self):
        self.client.portfolio.add_stock(self.portfolio_stock)
        self.assertEqual(len(self.client.portfolio.stocks), 1)
        self.assertEqual(self.client.portfolio.stocks[0].ticker_symbol, "AAPL")


    def test_order_flow(self):
        order_flow=OrderFlow("TestOrderFlow")
        order_flow.submit_order_ntimes(self.order,self.stock_exchange,10)
        self.assertEqual(len(self.engine.buy_heapq.get_order_list())+len(self.engine.sell_heapq.get_order_list()),10)
        



if __name__ == '__main__':
    unittest.main()




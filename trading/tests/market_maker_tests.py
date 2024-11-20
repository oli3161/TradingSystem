import sys
sys.path.append('C:/Users/ogigu/OneDrive/Documents/Ecole/Algo/TradingSystem/trading')  # Adjust to the actual path of the 'trading' folder

import unittest
from models import *


class MarketMaker(unittest.TestCase):

    def setUp(self):

        self.stock_exchange = StockExchange("Quebek")

        self.stock_exchange.addStockMarketListing("AAPL", "Apple Inc", 150.0)
        self.market_maker = self.stock_exchange.getMarketMaker("AAPL")
        self.order_matching_engine = self.market_maker.ordermatching_engine

        self.client_buyer = Client("JoeBlow")
        self.buyer_asset = Assets(money_amount=1000)


        self.client_seller = Client("PoorBobby")
        self.seller_stock = PortfolioStock("AAPL", 10, 120.0,150)
        self.seller_asset = Assets(self.seller_stock,0)

    def test_add_buy_order(self):

        order = Order("AAPL",100,400,"2021-01-01",Client("ClientName"),"buy",Assets(PortfolioStock("AAPL", 10, 150.0,120),1000))
        self.stock_exchange.submit_order(order)

        market_maker = self.stock_exchange.getMarketMaker("AAPL")
        self.assertIn(order, market_maker.ordermatching_engine.buy_heapq.get_order_list())

        print(self.order_matching_engine)

    def test_match_orders(self):

        order = Order("AAPL",100,5,"2021-01-01",Client("ClientName"),"buy",Assets(PortfolioStock("AAPL", 10, 150.0,120),1000))
        self.stock_exchange.submit_order(order)

        order = Order("AAPL",100,5,"2021-01-01",Client("ClientName"),"sell",Assets(PortfolioStock("AAPL", 10, 150.0,120),1000))
        self.stock_exchange.submit_order(order)

        self.order_matching_engine.match_orders()

        print(self.order_matching_engine)
        print(self.stock_exchange.stock_market_listings["AAPL"])

        self.assertEqual(self.order_matching_engine.buy_heapq.get_order_list(),[])
        self.assertEqual(self.order_matching_engine.sell_heapq.get_order_list(),[])



if __name__ == '__main__':
    unittest.main()
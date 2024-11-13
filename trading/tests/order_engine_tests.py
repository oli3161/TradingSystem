import sys
sys.path.append('C:/Users/ogigu/OneDrive/Documents/Ecole/Algo/TradingSystem/trading')  # Adjust to the actual path of the 'trading' folder

import unittest
from models import *


class TestOrderEngine(unittest.TestCase):

    def setUp(self):

        self.apple_stock = StockMarketListing("AAPL", "Apple Inc", 150.0,MarketMaker)
        
        self.engine = OrderMatchingEngine(self.apple_stock)

        self.client_buyer = Client("JoeBlow")
        self.buyer_asset = Assets(money_amount=1000)


        self.client_seller = Client("PoorBobby")
        self.seller_stock = PortfolioStock("AAPL", 10, 120.0,150)
        self.seller_asset = Assets(self.seller_stock,0)

    def test_add_buy_order(self):
        order = Order("AAPL",100,3,"2021-01-01",Client("ClientName"),"Buy",Assets(PortfolioStock("AAPL", 10, 150.0,120),1000))
        self.engine.add_buy_order(order)
        self.assertIn(order, self.engine.buy_heapq.get_order_list())

    def test_add_sell_order(self):
        order = Order("AAPL",100,3,"2021-01-01",Client("ClientName2"),"Sell",Assets(PortfolioStock("AAPL", 10, 150.0,120),0))
        self.engine.add_sell_order(order)
        self.assertIn(order, self.engine.sell_heapq.get_order_list())

    def test_match_order(self):

        # buy_order = Order("AAPL",100,3,"2021-01-01",Client("ClientName"),"Buy",Assets(PortfolioStock("AAPL", 10, 150.0,120),1000))
        # sell_order = Order("AAPL",100,3,"2021-01-01",Client("ClientName2"),"Sell",Assets(PortfolioStock("AAPL", 10, 150.0,120),0))
        buy_order = Order("AAPL",100,3,"2021-01-01",self.client_buyer,"Buy",self.buyer_asset)
        sell_order = Order("AAPL",100,3,"2021-01-01",self.client_seller,"Sell",self.seller_asset)

        self.engine.add_buy_order(buy_order)
        self.engine.add_sell_order(sell_order)
        self.engine.match_orders()
        
        self.assertNotIn(buy_order, self.engine.buy_heapq.get_order_list())
        self.assertNotIn(sell_order, self.engine.sell_heapq.get_order_list())
        

        self.assertEqual(buy_order.order_status, "Completed")
        self.assertEqual(sell_order.order_status, "Completed")

if __name__ == '__main__':
    unittest.main()
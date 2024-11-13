import sys
sys.path.append('C:/Users/ogigu/OneDrive/Documents/Ecole/Algo/TradingSystem/trading')  # Adjust to the actual path of the 'trading' folder

import unittest
from unittest.mock import Mock
from models import *


class TestOrderEngine(unittest.TestCase):

    def setUp(self):
        
        self.engine = OrderMatchingEngine(StockMarketListing("AAPL", "Apple Inc", 150.0,MarketMaker))

    def test_add_buy_order(self):
        order = Order(order_type="buy", price=100, quantity=10, price_type="Limit")
        self.engine.add_buy_order(order)
        self.assertIn(order, self.engine.buy_orders)

    def test_add_sell_order(self):
        order = Order(order_type="sell", price=100, quantity=10, price_type="Limit")
        self.engine.add_sell_order(order)
        self.assertIn(order, self.engine.sell_orders)

    def test_match_order(self):
        buy_order = Order(order_type="buy", price=100, quantity=10, price_type="Limit")
        sell_order = Order(order_type="sell", price=100, quantity=10, price_type="Limit")
        self.engine.add_buy_order(buy_order)
        self.engine.add_sell_order(sell_order)
        self.engine.match_orders()
        self.assertNotIn(buy_order, self.engine.buy_orders)
        self.assertNotIn(sell_order, self.engine.sell_orders)
        self.assertEqual(buy_order.quantity, 0)
        self.assertEqual(sell_order.quantity, 0)

    

if __name__ == '__main__':
    unittest.main()
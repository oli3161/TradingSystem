import unittest
from models import *


class TestOrderMatchingEngine(unittest.TestCase):
    
    def setUp(self):
        """Initialize the engine and create some orders."""
        # Create a mock stock listing
        self.stock_listing = Asset("AAPL", 150.00, 155.00)  # Initial bid and ask
        self.engine = OrderMatchingEngine(self.stock_listing)

        # Create mock clients and assets
        client1_assets = Assets(PortfolioStock("AAPL", 50, 150.00, 160.00), 5000)
        client2_assets = Assets(PortfolioStock("AAPL", 30, 140.00, 160.00), 3000)

        self.client1 = client1_assets
        self.client2 = client2_assets

        # Create limit and market orders
        self.limit_order_buy = LimitOrder("AAPL", price=150.00, quantity=10, client=Client(1), buy_order=True, assets=self.client1)
        self.limit_order_sell = LimitOrder("AAPL", price=155.00, quantity=5, client=Client(2), buy_order=False, assets=self.client2)
        self.market_order_buy = MarketOrder("AAPL", price=155.00, quantity=5, client=Client(1), buy_order=True, assets=self.client1)
        self.market_order_sell = MarketOrder("AAPL", price=150.00, quantity=5, client=Client(2), buy_order=False, assets=self.client2)

    def test_add_buy_order(self):
        """Test adding a buy order to the engine."""
        self.engine.add_buy_order(self.limit_order_buy)
        self.assertEqual(self.engine.buy_heapq.peek().price, 150.00)
        
    def test_add_sell_order(self):
        """Test adding a sell order to the engine."""
        self.engine.add_sell_order(self.limit_order_sell)
        self.assertEqual(self.engine.sell_heapq.peek().price, 155.00)

    def test_order_matching_limit_to_limit(self):
        """Test matching a buy limit order to a sell limit order."""
        self.engine.add_buy_order(self.limit_order_buy)
        self.engine.add_sell_order(self.limit_order_sell)

        # Match orders
        self.engine.match_orders()

        # Assert that the transaction was completed
        self.assertEqual(len(self.engine.transactions), 1)
        transaction = self.engine.transactions[0]
        self.assertEqual(transaction.price, 155.00)  # Transaction should be at the ask price

    def test_order_matching_limit_to_market(self):
        """Test matching a buy limit order to a sell market order."""
        self.engine.add_buy_order(self.limit_order_buy)
        self.engine.add_sell_order(self.market_order_sell)

        # Match orders
        self.engine.match_orders()

        # Assert that the transaction was completed
        self.assertEqual(len(self.engine.transactions), 1)
        transaction = self.engine.transactions[0]
        self.assertEqual(transaction.price, 150.00)  # Transaction price should be the limit order price

    def test_order_matching_market_to_limit(self):
        """Test matching a buy market order to a sell limit order."""
        self.engine.add_buy_order(self.market_order_buy)
        self.engine.add_sell_order(self.limit_order_sell)

        # Match orders
        self.engine.match_orders()

        # Assert that the transaction was completed
        self.assertEqual(len(self.engine.transactions), 1)
        transaction = self.engine.transactions[0]
        self.assertEqual(transaction.price, 155.00)  # Transaction price should be the limit order price

    def test_order_matching_market_to_market(self):
        """Test matching two market orders."""
        self.engine.add_buy_order(self.market_order_buy)
        self.engine.add_sell_order(self.market_order_sell)

        # Match orders
        self.engine.match_orders()

        # Assert that the transaction was completed with a midprice calculation
        self.assertEqual(len(self.engine.transactions), 1)
        transaction = self.engine.transactions[0]
        self.assertEqual(transaction.price, 152.50)  # Midprice between the two market orders with spread adjustment

    def test_partial_fill(self):
        """Test a partial fill of an order (quantity mismatch)."""
        # Add orders with different quantities
        self.engine.add_buy_order(self.limit_order_buy)
        self.engine.add_sell_order(self.limit_order_sell)

        # Only part of the sell order should be filled (5 out of 10 units)
        self.limit_order_buy.quantity = 5  # Adjust the buy order quantity
        self.engine.match_orders()

        # Assert that the transaction was completed
        self.assertEqual(len(self.engine.transactions), 1)
        transaction = self.engine.transactions[0]
        self.assertEqual(transaction.quantity, 5)  # Only 5 shares should have been traded

    def test_no_match(self):
        """Test the case where no orders can be matched."""
        # Add orders with non-overlapping prices
        self.engine.add_buy_order(self.limit_order_buy)
        self.engine.add_sell_order(self.limit_order_sell)

        # No match should happen because the buy price is less than the sell price
        self.engine.match_orders()

        # Assert that no transaction was created
        self.assertEqual(len(self.engine.transactions), 0)

    def test_transaction_update(self):
        """Test that the stock listing price updates after a transaction."""
        initial_price = self.stock_listing.last_price
        self.engine.add_buy_order(self.limit_order_buy)
        self.engine.add_sell_order(self.limit_order_sell)

        # Match orders
        self.engine.match_orders()

        # Assert that the stock price has been updated after the transaction
        self.assertEqual(self.stock_listing.last_price, 155.00)

    def test_spread_in_market_orders(self):
        """Test spread adjustment between market orders."""
        self.engine.add_buy_order(self.market_order_buy)
        self.engine.add_sell_order(self.market_order_sell)

        # Match market orders and verify that the price adjustment happens
        self.engine.match_orders()

        # Assert that the transaction price is correctly adjusted with the spread
        self.assertEqual(len(self.engine.transactions), 1)
        transaction = self.engine.transactions[0]
        self.assertEqual(transaction.price, 152.50)  # Midprice plus the spread adjustments

if __name__ == "__main__":
    unittest.main()
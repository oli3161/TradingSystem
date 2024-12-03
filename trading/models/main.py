import sys


sys.path.append('C:/Users/ogigu/OneDrive/Documents/Programming/Algo/TradingSystem/trading')  # Adjust to the actual path of the 'trading' folder

from models import *


stock_listing = StockMarketListing("AAPL", 150.00, 155.00)  # Initial bid and ask
engine = OrderMatchingEngine( stock_listing)

# Create mock clients and assets
client1_assets = Assets(PortfolioStock("AAPL", 50, 150.00, 160.00), 5000)
client2_assets = Assets(PortfolioStock("AAPL", 30, 140.00, 160.00), 3000)

client1 = client1_assets
client2 = client2_assets

# Create limit and market orders
limit_order_buy = LimitOrder("AAPL", price=150.00, quantity=10, client=Client(1), buy_order=True, assets= client1)
limit_order_sell = LimitOrder("AAPL", price=155.00, quantity=5, client=Client(2), buy_order=False, assets= client2)
market_order_buy = MarketOrder("AAPL", price=155.00, quantity=5, client=Client(1), buy_order=True, assets= client1)
market_order_sell = MarketOrder("AAPL", price=150.00, quantity=5, client=Client(2), buy_order=False, assets= client2)


engine.add_buy_order(limit_order_buy)
engine.add_sell_order(limit_order_sell)
engine.add_buy_order(market_order_buy)
engine.add_sell_order(market_order_sell)

engine.match_orders()
engine.print_transactions()
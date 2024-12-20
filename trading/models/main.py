import sys
import time

sys.path.append('C:/A/ETS/AlgoETS/Simulateur/TradingSystem/TradingSystem/trading')  # Adjust to the actual path of the 'trading' folder

from models import *



exchange = StockExchange('NYSE')
exchange.addStockMarketListing("AAPL", "Apple Inc.", 155.00)

# # # Create mock clients and assets
# client1_assets = Assets(PortfolioStock("AAPL", 50, 150.00, 160.00), 5000)
# client2_assets = Assets(PortfolioStock("AAPL", 30, 140.00, 160.00), 3000)

# client1 = client1_assets
# client2 = client2_assets

# Create OrderFlow instances
order_flow1 = OrderFlow(1)
order_flow2 = OrderFlow(2)


# Function to simulate stock market ticks
def simulate_market_ticks(stock_exchange : StockExchange, order_flow1 : OrderFlow, order_flow2 : OrderFlow, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        # Randomly create limit and market orders
        # limit_order = LimitOrder("AAPL", price=150.00, quantity=10, client=Client(1), buy_order=True, assets=client1)
        # market_order = MarketOrder("AAPL", price=155.00, quantity=5, client=Client(2), buy_order=False, assets=client2)
        
        
        # Randomize and submit orders
        order_flow1.submit_random_orders(stock_exchange, 10, 140.00, 160.00, "AAPL")
        order_flow2.submit_random_orders(stock_exchange, 10, 140.00, 160.00, "AAPL")
        
        
        # Match orders and print transactions
        engine = stock_exchange.getMarketMaker("AAPL").ordermatching_engine
        engine.match_orders()
        stock_exchange.getStockMarketListing("AAPL").visualize_ticker()

        # Wait for 1 second before the next tick
        time.sleep(1)



# Simulate market for 60 seconds
simulate_market_ticks(exchange, order_flow1, order_flow2, 300)
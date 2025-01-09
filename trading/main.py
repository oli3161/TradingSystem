import time
from trading.models import *



exchange = StockExchange('NYSE')
exchange.addStockMarketListing("AAPL", "Apple Inc.", Money(150.00))



# Create OrderFlow instances
order_flow1 = OrderFlow(1)
order_flow2 = OrderFlow(2)


# Function to simulate stock market ticks
def simulate_market_ticks(stock_exchange : StockExchange, order_flow1 : OrderFlow, order_flow2 : OrderFlow, duration):
    start_time = time.time()
    while time.time() - start_time < duration:        
        
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
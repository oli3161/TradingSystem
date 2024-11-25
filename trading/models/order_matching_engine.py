from .heaps import MinOrderHeap, MaxOrderHeap
from .order import Order
from .limit_order import LimitOrder
from .stock_market_listing import StockMarketListing
from .transaction import Transaction
from datetime import datetime
from .transaction_history import TransactionHistory
from .heaps import AbstractExecutionQueue

#TODO : Increment the money made by the engine with the spread when matching orders
#TODO : Switch the spread and money logic to the MarketMaker class
class OrderMatchingEngine:

    spread = 0.02
    money = 0


    def __init__(self,stock_listing :StockMarketListing):
        
        self.sell_heapq = MinOrderHeap()
        self.buy_heapq = MaxOrderHeap()

        self.instant_buy_orders = 0
        self.instant_sell_orders = 0

        self.stock_listing = stock_listing


    def add_sell_order(self, order : Order):
        
        self.sell_heapq.push(order)
        

    def add_buy_order(self, order : Order):
        
        self.buy_heapq.push(order)
        

    def match_orders(self):

        while not self.buy_heapq.is_empty() and not self.sell_heapq.is_empty():
            # Get the best buy and sell orders
            best_buy_order = self.buy_heapq.peek()
            best_sell_order = self.sell_heapq.peek()

            print(best_buy_order)
            print(best_sell_order)


            #Update the bid and ask prices
            self.stock_listing.update_bid_price(best_buy_order.price)
            self.stock_listing.update_ask_price(best_sell_order.price)
            
            # Check if the orders can be matched
            if best_buy_order.price >= best_sell_order.price:

                
                # Match the orders
                self.complete_transaction(best_sell_order,best_buy_order,best_buy_order.price)
                
            elif isinstance(best_buy_order,LimitOrder) and isinstance(best_sell_order,LimitOrder) :

                self.match_limit_market_orders(best_sell_order,best_buy_order)

            elif isinstance(best_buy_order,Order) and isinstance(best_sell_order,Order) :

                self.match_market_orders(best_buy_order,best_sell_order)

            else:
                break

    #Used to match two market orders with prices that are far from each other
    def match_market_orders(self,sell_order : Order,buy_order : Order):

        #Calculate the fair midprice between two market orders
        midprice = (sell_order.price + buy_order.price) / 2

        #Adjust the prices of the buy order
        adjusted_buy_price = midprice + self.spread / 2
        buy_order.price = adjusted_buy_price 

        #Adjust the prices of the sell order
        adjusted_sell_price = midprice - self.spread / 2
        sell_order.price = adjusted_sell_price

        self.complete_transaction(sell_order,buy_order,midprice)        


    #Used to match a limit order with a market order
    def match_limit_market_orders(self,limit_order : Order, market_order : Order):
        pass
        

    def complete_transaction(self,sell_order : Order,buy_order : Order,price):

        
        sell_order_quantity = sell_order.remaining_quantity
        buy_order_quantity = buy_order.remaining_quantity 

        #If the quantities are not equal, we need to adjust the quantities
        if  sell_order_quantity != buy_order_quantity :

            trade_quantity = min(sell_order_quantity,buy_order_quantity)

        #If the quantities are equal, we can just transfer the shares and money
        else:
                trade_quantity = sell_order_quantity

        
        #Transfer the shares first
        sellers_shares = sell_order.remove_shares(trade_quantity,price)
        
        buy_order.add_shares(sellers_shares,price)

        #Transfer the money value
        money_value = buy_order.remove_money(trade_quantity * price)
        sell_order.asset.add_money(money_value)

        #Update the price of the stock_listing
        self.stock_listing.update_price(price)

        #Update instant count values for the buy/sell
        self.instant_buy_orders -= buy_order_quantity
        self.instant_sell_orders -= sell_order_quantity

        # Create Transaction instance
        transaction = Transaction(
            ticker=sell_order.ticker,
            price=price,
            quantity=trade_quantity,
            transaction_date=datetime.now(),
            buyer=buy_order.client,
            seller=sell_order.client,
            transaction_type=True,
            total_value=trade_quantity * price
        )
        transaction_history = TransactionHistory()
        transaction_history.add_transaction(transaction)

        #If the order is fully executed, remove it from the heap
        if sell_order.remaining_quantity == 0:
            self.sell_heapq.pop()
        if buy_order.remaining_quantity == 0:
            self.buy_heapq.pop()
    

    def __str__(self):
        
        best_bid = self.stock_listing.bid_price
        best_ask = self.stock_listing.ask_price

        instant_buy_orders = self.instant_buy_orders
        instant_sell_orders = self.instant_sell_orders

        return f"Best Bid: {best_bid} Best Ask: {best_ask} Instant Buy Orders: {instant_buy_orders} Instant Sell Orders: {instant_sell_orders}"
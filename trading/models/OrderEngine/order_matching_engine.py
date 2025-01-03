from .order_engine import OrderEngine
from trading.models.order import Order
from trading.models.limit_order import LimitOrder
from trading.models.market_order import MarketOrder
from trading.models.Assets.stock_market_listing import Asset
from trading.models.transaction import Transaction
from datetime import datetime
from .order_engine import OrderMatchingEngineFactory
from trading.models.money import Money

#TODO : Increment the money made by the engine with the spread when matching orders
#TODO : Switch the spread and money logic to the MarketMaker class

class SimulatedOrderMatchingEngineFactory(OrderMatchingEngineFactory):
    def create_order_matching_engine(self, stock_market_listing):
        return SimulatedOrderMatchingEngine(stock_market_listing)


class SimulatedOrderMatchingEngine(OrderEngine):

    spread = 0.02
    money = 0


    def __init__(self,stock_listing :Asset):
        OrderEngine.__init__(self,stock_listing)
    

    def update_quotes(self):
        """
        Updates the bid and ask prices in the stock listing.
        """
        best_bid_order = self.buy_heapq.peek()
        best_ask_order = self.sell_heapq.peek()

        if best_bid_order is not None:
            self.stock_listing.update_bid_price(best_bid_order.price)
        if best_ask_order is not None:
            self.stock_listing.update_ask_price(best_ask_order.price)
        

    def match_orders(self):
        """
        Matches buy and sell orders from the respective priority queues.
        """
        self.buy_heapq.initialize_matching_state()
        self.sell_heapq.initialize_matching_state()

        while not self.buy_heapq.top_orders_verified() and not self.sell_heapq.top_orders_verified():
            
            
            # Get the best buy and sell orders
            best_buy_order = self.buy_heapq.peek()
            best_sell_order = self.sell_heapq.peek()

            if best_buy_order is None or best_sell_order is None:
                break


            # Check if orders can be matched if both are limit orders
            if isinstance(best_buy_order, LimitOrder) and isinstance(best_sell_order, LimitOrder) and best_buy_order.price >= best_sell_order.price:
                # Match buy and sell orders
                self.match_limit_orders(best_buy_order, best_sell_order)

            elif isinstance(best_buy_order, LimitOrder) and isinstance(best_sell_order, MarketOrder):
                self.match_limit_market_orders(best_buy_order, best_sell_order)

            elif isinstance(best_buy_order, MarketOrder) and isinstance(best_sell_order, LimitOrder):
                self.match_limit_market_orders(best_sell_order, best_buy_order)

            elif isinstance(best_buy_order, MarketOrder) and isinstance(best_sell_order, MarketOrder):
                self.match_market_orders(best_sell_order,best_buy_order)

            else:
                # No matching possible for current best orders
                if  isinstance(best_buy_order,LimitOrder):
                    self.buy_heapq.limit_orders_verified()
                if  isinstance(best_sell_order,LimitOrder):
                    self.sell_heapq.limit_orders_verified()
                    
        self.buy_heapq.initialize_matching_state()
        self.sell_heapq.initialize_matching_state()
        self.update_quotes()
           

    def match_limit_orders(self,buy_order : Order,sell_order : Order):

        stock_price = self.stock_listing.last_price
        # stock_price = Decimal(stock_price)  # Convert once

        if abs(stock_price.amount - buy_order.price.amount) < abs(stock_price.amount - sell_order.price.amount):
            
            transaction_price = buy_order.price
        else:
            transaction_price = sell_order.price

        # if buy_order.asset.money < buy_order.remaining_quantity * transaction_price:
        #     print(f"buy order cannot buy {self.stock_listing.ticker_symbol} showing {self.stock_listing.last_price} at {transaction_price}")
        #     print("buy order : " + str(buy_order))

        self.complete_transaction(sell_order,buy_order,transaction_price)
        


    #Used to match two market orders with prices that are far from each other
    def match_market_orders(self,sell_order : Order,buy_order : Order):

        #Calculate the fair midprice between two market orders
        midprice = (sell_order.price + buy_order.price) / 2

        #Adjust the prices of the buy order
        price_adjusted = buy_order.adjust_price(midprice)
        if price_adjusted == False:
            return

        #Adjust the prices of the sell order
        sell_order.price = midprice

        self.complete_transaction(sell_order,buy_order,midprice)        

    #TODO Add verification that the market Order has enough money in the assets to buy the shares, if not, remove order and change status to cancelled
    #Used to match a limit order with a market order
    def match_limit_market_orders(self, limit_order: Order, market_order: Order):
        """
        Matches a limit order with a market order. Adjusts the market order's price 
        to the limit order's price and updates the bid/ask prices in the stock listing.
        
        Args:
            limit_order (Order): The limit order (buy or sell).
            market_order (Order): The market order (buy or sell).
        """
        # Adjust the market order's price to the limit order's price
        price_adjusted = market_order.adjust_price(limit_order.price)
        if price_adjusted == False:
            return

        # Update the stock listing bid/ask prices based on the type of limit order
        # if limit_order.is_buy_order():
        #     self.stock_listing.update_bid_price(limit_order.price)
        # else:
        #     self.stock_listing.update_ask_price(limit_order.price)

        # Proceed to complete the transaction using the adjusted market order
        self.complete_transaction(
            sell_order=market_order if not market_order.is_buy_order() else limit_order,
            buy_order=limit_order if limit_order.is_buy_order() else market_order,
            price=limit_order.price  # The transaction price is the limit order's price
        )

        

    def complete_transaction(self,sell_order : Order,buy_order : Order,price : Money):

        
        sell_order_quantity = sell_order.remaining_quantity
        buy_order_quantity = buy_order.remaining_quantity 

        # Determine the trade quantity
        trade_quantity = min(sell_order_quantity, buy_order_quantity)

        # Calculate the total transaction cost
        total_cost = price * trade_quantity

        #Transfer the shares
        sellers_shares = sell_order.remove_shares(trade_quantity,price)
        buy_order.add_shares(sellers_shares,price)

        #Transfer the money first value
        if buy_order.asset.money < total_cost:
            print("Here")
        money_value = buy_order.remove_money(total_cost)
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
            total_value=trade_quantity * price.amount
        )
        self.transactions.append(transaction)

        #If the order is fully executed, remove it from the heap
        # if sell_order.remaining_quantity == 0:
        #     self.sell_heapq.pop()
        # if buy_order.remaining_quantity == 0:
        #     self.buy_heapq.pop()
    

    def __str__(self):
        
        best_bid = self.stock_listing.bid_price
        best_ask = self.stock_listing.ask_price

        instant_buy_orders = self.instant_buy_orders
        instant_sell_orders = self.instant_sell_orders

        return f"Best Bid: {best_bid} Best Ask: {best_ask} Instant Buy Orders: {instant_buy_orders} Instant Sell Orders: {instant_sell_orders}"
    
    def print_transactions(self):
        for transaction in self.transactions:
            print(transaction)
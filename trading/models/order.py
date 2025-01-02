from .assets import Assets
from .constants import ORDER_STATUS_PENDING, ORDER_STATUS_COMPLETED, ORDER_STATUS_CANCELLED
from datetime import datetime


class Order :

    def __init__(self, ticker,price, quantity, client,buy_order,assets : Assets, order_status = ORDER_STATUS_PENDING) :
        
        self.order_date = datetime.now()
        self.order_status = order_status # Can be "Pending", "Completed", "Cancelled"
        self.client = client
        self.price=price
        self.ticker = ticker
        self.remaining_quantity = quantity
        self.initial_quantity = quantity
        self.buy_order = buy_order        # Can only be True or False, if False then it is a sell order
        self.asset : Assets = assets

    def is_buy_order(self):
        return self.buy_order

    def complete_order(self) :
        
        self.order_status = ORDER_STATUS_COMPLETED
        
        #Notifies the client
        self.client.notify_completed_order(self)

    def adjust_price(self, price):

        if price * self.remaining_quantity > self.asset.money_amount:
            self.notify_order_cancelled("Not enough money in the account")
            return False
        else:
            self.price = price
            return True

    def add_shares(self, quantity, price):
        self.asset.add_shares(quantity, price)
        
        #Remove quantity processed from order
        self.decrease_quantity_traded(quantity)

    def remove_shares(self, quantity, price):
        shares = self.asset.remove_shares(quantity, price)

        #Remove quantity processed from order
        self.decrease_quantity_traded(quantity)

        return shares
    
    def add_money(self, amount):
        self.asset.add_money(amount)

    def remove_money(self, amount):
        money = self.asset.remove_money(amount)

        if money < amount:
            self.notify_order_cancelled("Not enough money in the account")
            return None
        return money
    
    def notify_order_cancelled(self,reason):
        
        # print(f"Order {self} was cancelled because {reason}")
        self.order_status = ORDER_STATUS_CANCELLED
    
    

    def decrease_quantity_traded(self, quantity):
        self.remaining_quantity -= quantity

        if self.remaining_quantity == 0:
            self.complete_order()
    
    # def adjust_quantity(self, quantity):
    #     self.remaining_quantity = quantity
    #     self.initial_quantity = quantity

    def is_cancelled(self):
        """Checks if the order is cancelled."""
        return self.order_status == ORDER_STATUS_CANCELLED

    def is_pending(self):
        """Checks if the order is still pending."""
        return self.order_status == ORDER_STATUS_PENDING

    def is_completed(self):
        """Checks if the order has been completed."""
        return self.order_status == ORDER_STATUS_COMPLETED

    def __str__(self):
        return (f"Order(ticker={self.ticker}, price={self.price}, quantity={self.initial_quantity}, "
                f"order_date={self.order_date}, client={self.client}, order_type=Order, "
                f"order_status={self.order_status}, asset={self.asset})")
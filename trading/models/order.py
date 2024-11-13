# from .client import Client
from .assets import Assets
import random

class Order :

    def __init__(self, ticker, quantity, order_date, client,order_type,assets : Assets, order_status = "Pending") :
        
        self.order_date = order_date
        self.order_status = order_status
        self.client = client
        
        self.ticker = ticker
        self.remaining_quantity = quantity
        self.initial_quantity = quantity
        self.order_type = order_type        # Can only be "Buy" or "Sell"
        self.asset : Assets = assets


    def complete_order(self) :
        
        self.order_status = "Completed"
        
        #Notifies the client
        self.client.notify_completed_order(self)

    def add_shares(self, quantity, price):
        self.asset.add_shares(quantity, price)
        
        #Remove quantity processed from order
        self.remaining_quantity -= quantity

    def remove_shares(self, quantity, price):
        shares = self.asset.remove_shares(quantity, price)

        #Remove quantity processed from order
        self.remaining_quantity -= quantity

        return shares

    def remove_money(self, amount):
        money = self.asset.remove_money(amount)

        return money
    

    def add_money(self, amount):
        self.asset.add_money(amount)

    def decrease_quantity_traded(self, quantity):
        self.remaining_quantity -= quantity

        if self.remaining_quantity == 0:
            self.complete_order()

    def __str__(self):
        return (f"Order(ticker={self.ticker}, price={self.price}, quantity={self.initial_quantity}, "
                f"order_date={self.order_date}, client={self.client}, order_type={self.order_type}, "
                f"price_type={self.price_type}, order_status={self.order_status}, asset={self.asset})")
    

   
# from .client import Client
from .assets import Assets
from datetime import datetime


class Order :

    def __init__(self, ticker,price, quantity, client,buy_order,assets : Assets, order_status = "Pending") :
        
        self.order_date = datetime.now()
        self.order_status = order_status
        self.client = client
        self.price=price
        self.ticker = ticker
        self.remaining_quantity = quantity
        self.initial_quantity = quantity
        self.buy_order = buy_order        # Can only be True or False, if False then it is a sell order
        self.asset : Assets = assets

    def is_buy_order(self):
        return self.buy_order

    def is_sell_order(self):
        return self.buy_order

    def complete_order(self) :
        
        self.order_status = "Completed"
        
        #Notifies the client
        self.client.notify_completed_order(self)

    def add_shares(self, quantity, price):
        self.asset.add_shares(quantity, price)
        
        #Remove quantity processed from order
        self.decrease_quantity_traded(quantity)

    def remove_shares(self, quantity, price):
        shares = self.asset.remove_shares(quantity, price)

        #Remove quantity processed from order
        self.decrease_quantity_traded(quantity)

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
                f"order_date={self.order_date}, client={self.client}, "
                f"order_status={self.order_status}, asset={self.asset})")
    

   

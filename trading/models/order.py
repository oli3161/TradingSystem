from .assets import Assets
from .constants import ORDER_STATUS_PENDING, ORDER_STATUS_COMPLETED, ORDER_STATUS_CANCELLED
from datetime import datetime
from .money import Money


class Order:
    def __init__(self, ticker, price: Money, quantity, client, buy_order, assets: Assets, order_status=ORDER_STATUS_PENDING):
        """
        Initialize an Order.
        
        :param ticker: The stock ticker for the order.
        :param price: The price per share as a Money object.
        :param quantity: The number of shares for the order.
        :param client: The client who placed the order.
        :param buy_order: Boolean, True for buy orders, False for sell orders.
        :param assets: The client's assets involved in the order.
        :param order_status: The status of the order (default: Pending).
        """
        self.order_date = datetime.now()
        self.order_status = order_status
        self.client = client
        self.ticker = ticker
        self.remaining_quantity = quantity
        self.initial_quantity = quantity
        self.buy_order = buy_order
        self.asset: Assets = assets

        if isinstance(price, Money):
            self.price = price

        elif isinstance(price, float) or isinstance(price, int):
            self.price = Money(price)

        else:
            raise ValueError("Price must be a Money object or a number.")

    def is_buy_order(self):
        return self.buy_order

    def complete_order(self):
        self.order_status = ORDER_STATUS_COMPLETED
        self.client.notify_completed_order(self)

    def adjust_price(self, price: Money):
        """
        Adjust the price of the order.
        Ensures the buyer has enough money to cover the cost if it's a buy order.
        """
        total_cost = price * self.remaining_quantity
        if self.is_buy_order() and total_cost > self.asset.money:
            self.notify_order_cancelled("Not enough money in the account")
            return False
        else:
            self.price = price
            return True

    def add_shares(self, quantity, price: Money):
        self.asset.add_shares(quantity, price)
        self.decrease_quantity_traded(quantity)

    def remove_shares(self, quantity, price: Money):
        shares = self.asset.remove_shares(quantity, price)
        self.decrease_quantity_traded(quantity)
        return shares

    def add_money(self, money: Money):
        self.asset.add_money(money)

    def remove_money(self, money: Money):
        if self.asset.money < money:
            self.notify_order_cancelled("Not enough money in the account")
            return None
        return self.asset.remove_money(money)

    def notify_order_cancelled(self, reason):
        """Cancel the order and set the status to cancelled."""
        self.order_status = ORDER_STATUS_CANCELLED

    def decrease_quantity_traded(self, quantity):
        """Decrease the remaining quantity of the order."""
        self.remaining_quantity -= quantity
        if self.remaining_quantity == 0:
            self.complete_order()

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
                f"order_date={self.order_date}, client={self.client}, buy_order={self.buy_order}, "
                f"order_status={self.order_status}, asset={self.asset})")

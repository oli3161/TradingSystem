from .portfolio_stock import PortfolioStock
from .money import Money

class Assets:


    def __init__(self , portfolio_stock : PortfolioStock = PortfolioStock(), money = Money(0)):
        
        self.portfolio_stock : PortfolioStock = portfolio_stock
        self.money : Money = money

    def add_stock(self, portfolio_stock : PortfolioStock):
        self.portfolio_stock = portfolio_stock

    def add_shares(self, quantity, price):
        self.portfolio_stock.add_shares(quantity, price)
        
    def remove_shares(self, quantity, price):
        if self.portfolio_stock.shares_owned < quantity:
            raise ValueError("Not enough shares in the account")
        shares = self.portfolio_stock.remove_shares(quantity, price)

        return shares

    def add_money(self, amount: Money):
        if self.money.currency != amount.currency:
            raise ValueError("Currency mismatch.")
        self.money += amount

    def remove_money(self, amount: Money):
        if self.money.currency != amount.currency:
            raise ValueError("Currency mismatch.")
        if self.money < amount:
            raise ValueError("Not enough money in the account")
        self.money -= amount
        return amount

    def __str__(self):
        return (f"Assets(portfolio_stock={self.portfolio_stock}, money={self.money})")
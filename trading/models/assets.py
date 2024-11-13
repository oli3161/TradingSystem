from .portfolio_stock import PortfolioStock


class Assets:


    def __init__(self , portfolio_stock : PortfolioStock = PortfolioStock(), money_amount = 0):
        
        self.portfolio_stock : PortfolioStock = portfolio_stock
        self.money_amount = money_amount

    def add_stock(self, portfolio_stock : PortfolioStock):
        self.portfolio_stock = portfolio_stock

    def add_shares(self, quantity, price):
        self.portfolio_stock.add_shares(quantity, price)
        
    def remove_shares(self, quantity, price):
        if self.portfolio_stock.shares_owned < quantity:
            raise ValueError("Not enough shares in the account")
        shares = self.portfolio_stock.remove_shares(quantity, price)

        return shares

    def add_money(self, amount):
        self.money_amount += amount

    def remove_money(self, amount):
        if self.money_amount < amount:
            raise ValueError("Not enough money in the account")
        self.money_amount -= amount
        return amount
    
    def __str__(self):
        return (f"Assets(portfolio_stock={self.portfolio_stock}, money_amount={self.money_amount})")
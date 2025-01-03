from typing import List
from .portfolio_stock import PortfolioStock



class Portfolio:

    def __init__(self):

        self.stocks : List[PortfolioStock] = []

    def add_stock(self, stock : PortfolioStock):
        self.stocks.append(stock)


    def __str__(self):
        stocks_str = ', '.join(str(stock) for stock in self.stocks)
        return f"Portfolio with {len(self.stocks)} stocks: [{stocks_str}]"
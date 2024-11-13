class PortfolioStock:

    def __init__(self, ticker_symbol, shares_owned, average_purchase_price,
                  market_price):
        self.ticker_symbol = ticker_symbol
        self.shares_owned = shares_owned
        self.average_purchase_price = average_purchase_price
        self.market_price = market_price
        self.total_invested = shares_owned * average_purchase_price
        self.unrealized_gain_loss = (market_price - average_purchase_price) * shares_owned
    

    def add_shares(self,quantity,price):

        new_value = quantity * price

        self.total_invested += new_value
        self.shares_owned += quantity
        self.average_purchase_price = self.total_invested / self.shares_owned
        self.unrealized_gain_loss = (self.market_price - self.average_purchase_price) * self.shares_owned

    def remove_shares(self,quantity,price):

        new_value = quantity * price

        self.total_invested -= new_value
        self.shares_owned -= quantity
        self.average_purchase_price = self.total_invested / self.shares_owned
        self.unrealized_gain_loss = (self.market_price - self.average_purchase_price) * self.shares_owned

        return quantity

    def __str__(self):
        return (f"Ticker: {self.ticker_symbol}, Shares: {self.shares_owned}, "
                f"Avg Purchase Price: {self.average_purchase_price}, "
                f"Market Price: {self.market_price}, "
                f"Total Invested: {self.total_invested}, "
                f"Unrealized Gain/Loss: {self.unrealized_gain_loss}")


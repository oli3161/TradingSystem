from models.orderbook import OrderBook


class StockMarketListing:

    def __init__(self, ticker_symbol, company_name, last_price):
        self.ticker_symbol = ticker_symbol
        self.company_name = company_name
        self.bid_price = last_price
        self.ask_price = last_price
        self.last_price = last_price
        self.order_book : OrderBook = OrderBook()



    def update_price(self,price):
       
        self.last_price = price

    def update_bid_price(self,price):
        self.bid_price = price

    def update_ask_price(self,price):
        self.ask_price = price
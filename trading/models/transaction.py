from datetime import datetime

class Transaction:
    def __init__(self, ticker, price, quantity, transaction_date, buyer, seller, transaction_type, total_value):
        self.ticker = ticker
        self.price = price
        self.quantity = quantity
        self.transaction_date = transaction_date
        self.buyer = buyer            # Buyer is the Client object from the buy_order
        self.seller = seller          # Seller is the Client object from the sell_order
        self.transaction_type = transaction_type  # True or False
        self.total_value = total_value            # Total value of the transaction (price * quantity)
    
    def __str__(self):
        return (f"Transaction(ticker={self.ticker}, price={self.price}, quantity={self.quantity}, "
                f"transaction_date={self.transaction_date}, buyer={self.buyer}, "
                f"seller={self.seller}, transaction_type={self.transaction_type}, total_value={self.total_value})")

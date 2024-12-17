from .order import Order
from .limit_order import LimitOrder
from .market_order import MarketOrder
from .stock_exchange import StockExchange
from .client import Client
from .assets import Assets
from .portfolio_stock import PortfolioStock
import random

class OrderFlow(Client):

    def __init__(self, id):
        Client.__init__(self, id)

    def submit_random_orders(self, stock_exchange: StockExchange, n: int, min_price, max_price, ticker: str):
        for i in range(n):
            order = self.create_random_order(min_price, max_price, ticker)
            stock_exchange.submit_order(order)

    def create_random_order(self, min_price, max_price, ticker: str):
        fake_client = Client(id=random.randint(1, 1000))
        buy_order = random.choice([True, False])
        order_type = random.choice([LimitOrder, MarketOrder])
        order = order_type(
            ticker=ticker,
            price=random.uniform(min_price, max_price),
            quantity=random.randint(1, 100),
            client=fake_client,
            buy_order=buy_order,
            assets=Assets()
        )
        self.adjust_assets(order)
        if order.buy_order and order.asset.money_amount == 0:
            print("ERRRORRRR")
            return None
        return order

    def adjust_assets(self, order: Order):
        if order.buy_order:
            # Ensure money_amount is added for buy orders
            order.asset = Assets(money_amount=order.price * order.initial_quantity * 10)
        else:
            # Ensure PortfolioStock is added for sell orders
            order.asset = Assets(portfolio_stock=PortfolioStock(order.ticker, order.initial_quantity))
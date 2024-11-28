from trading.models.order import Order
from trading.models.portfolio import Portfolio
from trading.models.stock_exchange import StockExchange
from mypy_extensions import NoReturn
from typing import Union


class Client:

    def __init__(self, id: Union[int, str]) -> NoReturn:
        self.id = id
        self.portfolio: Portfolio = Portfolio()

    def submit_order(self, order: Order, stock_exchange: StockExchange):

        stock_exchange.submit_order(order)

    def notify_completed_order(self, order: Order, verbose=False):

        self.portfolio.add_stock(order.asset.portfolio_stock)

        if verbose:
            print(order)

    def __str__(self) -> str:
        return f"Client(id={self.id})"

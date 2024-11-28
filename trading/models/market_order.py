
from trading.models.assets import Assets
from trading.models.order import Order


class MarketOrder(Order):

    def __init__(
        self,
        ticker,
        price,
        quantity,
        client,
        buy_order,
        assets: Assets,
        order_status="Pending",
    ):

        Order.__init__(
            self, ticker, price, quantity, client, buy_order, assets, order_status
        )

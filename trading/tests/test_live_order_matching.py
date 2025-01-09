import pytest
from ..models import *



# def test_buy_nvidia():

#     stock_exchange = StockExchange("Quebek")


#     live_exchange = LiveStockExchange(stock_exchange)

#     oli = Client(1)
#     assets = Assets(money=Money(10000))
#     order = MarketOrder("NVDA", Money(100), 10, oli, True, assets)

#     live_exchange.submit_order(order)
#     live_exchange.match_orders()

#     print(order.asset.portfolio_stock.total_invested)
#     print("Average purshase price : " , order.asset.portfolio_stock.average_purchase_price)
#     assert order.asset.portfolio_stock.average_purchase_price != 0, "Average purchase price should be updated"




# def test_sell_nvidia():

#     stock_exchange = StockExchange("Quebek")


#     live_exchange = LiveStockExchange(stock_exchange)

#     oli = Client(1)
#     assets = Assets(portfolio_stock=PortfolioStock("NVDA", 10))
#     order = MarketOrder("NVDA", Money(100), 10, oli, False, assets)

#     live_exchange.submit_order(order)
#     live_exchange.match_orders()

#     print(order.asset.money.amount)
#     assert order.asset.money.amount != 0, "Money should be updated"


def test_buy_multiple_tickers():

    stock_exchange = StockExchange("Quebek")


    live_exchange = LiveStockExchange(stock_exchange)

    oli = Client(1)
    assets = Assets(money=Money(10000))
    order = MarketOrder("NVDA", Money(100), 10, oli, True, assets)
    order2 = MarketOrder("TD.TO", Money(100), 10, oli, True, assets)
    order3 = MarketOrder("SHOP.TO", Money(100), 10, oli, True, assets)
    order4 = MarketOrder("TSLA", Money(100), 10, oli, True, assets)
    order5 = MarketOrder("Erorfmsf3", Money(100), 10, oli, True, assets)

    live_exchange.submit_order(order)
    live_exchange.submit_order(order2)
    live_exchange.submit_order(order3)
    live_exchange.submit_order(order4)
    live_exchange.submit_order(order5)
    
    live_exchange.match_orders()

    # print(order.asset.portfolio_stock.total_invested)
    # print("Average purshase price : " , order.asset.portfolio_stock.average_purchase_price)
    print(oli.portfolio)
    assert order.asset.portfolio_stock.average_purchase_price != 0, "Average purchase price should be updated"


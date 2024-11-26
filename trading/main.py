import asyncio
from models import *
from websockets.asyncio.server import serve, ServerConnection


async def on_connection(websocket: ServerConnection):
    async for message in websocket:
        await websocket.send(message)

async def main():
    stock_exchange = StockExchange("Quebek")

    stock_exchange.addStockMarketListing("AAPL", "Apple Inc", 150.0)
    market_maker = stock_exchange.getMarketMaker("AAPL")
    order_matching_engine = market_maker.ordermatching_engine

    client_buyer = Client("JoeBlow")
    buyer_asset = Assets(money_amount=1000)


    client_seller = Client("PoorBobby")
    seller_stock = PortfolioStock("AAPL", 10, 120.0,150)
    seller_asset = Assets(seller_stock,0)

    async with serve(on_connection, "0.0.0.0", 8765) as server:
        await server.serve_forever() 

if __name__ == "__main__":
    asyncio.run(main())

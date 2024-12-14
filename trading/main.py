import asyncio

from models import Assets, Client, PortfolioStock, StockExchange
from websocket_server import WebSocketServer


async def main():
    exchange = StockExchange("NYSE")
    exchange.addStockMarketListing("AAPL", "Apple Inc.", 155.00)

    client_assets = Assets(PortfolioStock("AAPL", 50), 5000)
    client = Client(1)

    server = WebSocketServer(exchange, client, client_assets)

    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())

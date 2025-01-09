import asyncio
from models import *
from websockets.asyncio.server import serve, ServerConnection

import asyncio
import websockets

class WebSocketServerRepository:
    connections: dict[str, ServerConnection]

    def __init__(self):
        self.connections = {}

    def add_connection(self, websocket: ServerConnection, username: str):
        identifier = f"{username}@{websocket.remote_address[0]}:{websocket.remote_address[1]}"

        self.connections[identifier] = websocket

        print(f"New connection added: {identifier}")

        return identifier

    async def remove_connection(self, identifier):
        if identifier in self.connections:
            await self.connections[identifier].close()

            del self.connections[identifier]

    async def send_message(self, identifier, message):
        if identifier not in self.connections:
            return
        
        websocket = self.connections[identifier]

        await websocket.send(message)

async def handle_client(websocket: ServerConnection, repo: WebSocketServerRepository):
    if not websocket.request:
        await websocket.close()
        return

    username = websocket.request.path.split("/", 1)[1]

    if username == "":
        await websocket.close()
        return

    identifier = repo.add_connection(websocket, username)

    try:
        async for message in websocket:
            print(message)
    
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection with {identifier} closed unexpectedly: {e}")
    except Exception as e:
        print(f"Error in connection with {identifier}: {e}")
    finally:
        await repo.remove_connection(identifier)

async def main():
    websocketRepo = WebSocketServerRepository()

    async with serve(lambda ws: handle_client(ws, websocketRepo), "0.0.0.0", 8765) as server:
        await server.serve_forever() 

if __name__ == "__main__":
    asyncio.run(main())


# main Mikael
# import asyncio

# from models import Assets, Client, PortfolioStock, StockExchange
# from websocket_server import WebSocketServer


# async def main():
#     exchange = StockExchange("NYSE")
#     exchange.addStockMarketListing("AAPL", "Apple Inc.", 155.00)

#     client_assets = Assets(PortfolioStock("AAPL", 50), 5000)
#     client = Client(1)

#     server = WebSocketServer(exchange, client, client_assets)

#     await server.serve_forever()


# if __name__ == "__main__":
#     asyncio.run(main())

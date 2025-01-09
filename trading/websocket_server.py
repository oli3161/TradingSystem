import websockets
from websockets.asyncio.server import ServerConnection, serve

from lib.in_memory_repository import InMemoryRepository
from models import Assets, Client, LimitOrder, StockExchange


class WebSocketServer:
    host: str
    port: int

    client: Client
    client_assets: Assets
    client_repo: InMemoryRepository[ServerConnection]
    exchange: StockExchange

    def __init__(
        self,
        exchange: StockExchange,
        client: Client,
        client_assets: Assets,
        host="0.0.0.0",
        port=8765,
    ):
        self.host = host
        self.port = port

        self.client_repo = InMemoryRepository()
        self.exchange = exchange
        self.client = client
        self.client_assets = client_assets

    async def serve_forever(self):
        async with serve(self.handle_client, self.host, self.port) as server:
            print("WSS running on 0.0.0.0:8765")
            await server.serve_forever()

    async def handle_client(self, websocket: ServerConnection):
        if not websocket.request:
            await websocket.close()
            return

        username = websocket.request.path.split("/", 1)[1]

        if username == "":
            await websocket.close()
            return

        identifier = self.client_repo.add(websocket)

        try:
            async for message in websocket:
                self.handle_message(str(message))

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection with {identifier} closed unexpectedly: {e}")
        except Exception as e:
            print(f"Error in connection with {identifier}: {e}")
        finally:
            await websocket.close()
            self.client_repo.delete(identifier)

    def handle_message(self, message: str):
        split_message = message.split(":")

        if len(split_message) < 4:
            return

        [action, stock, quantity, price] = split_message

        is_buy = False

        match action:
            case "BUY":
                is_buy = True
            case "SELL":
                is_buy = False
            case _:
                return

        if stock != "AAPL":
            return

        quantity = int(quantity)

        if quantity != quantity:
            return

        price = float(price)

        if price != price:
            return

        order = LimitOrder(
            stock, price, quantity, self.client, is_buy, self.client_assets
        )
        print(message)

        self.exchange.submit_order(order)

        engine = self.exchange.getMarketMaker("AAPL").ordermatching_engine
        engine.match_orders()

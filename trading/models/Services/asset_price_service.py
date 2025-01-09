from abc import ABC, abstractmethod


class AssetPriceService(ABC):

    @abstractmethod
    def get_price(self, asset_symbol: str) -> float:
        pass

    @abstractmethod
    def get_tickers_price(self, tickers: list) -> dict:
        pass
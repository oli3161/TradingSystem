from abc import ABC, abstractmethod
from ..order import Order



class MarketMaker(ABC):
    
    @abstractmethod
    def process_order(self,order : Order):
        pass
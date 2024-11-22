from .assets import Assets
from .order import Order

class MarketOrder(Order) :

    def __init__(self) :
        
        Order.__init__(self)
from .transaction import Transaction
from typing import List


class TransactionHistoryMeta(type):


    _instances = {}

    def __call__(cls, *args, **kwds):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwds)
            cls._instances[cls] = instance 

        return cls._instances[cls]
    

class TransactionHistory(metaclass = TransactionHistoryMeta):

    def __init__(self):
        self.transactions : List[Transaction] = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

 
from enum import StrEnum, auto

from ..asset import Asset


class BalanceType(StrEnum):
    DEBIT = auto()
    CREDIT = auto()


class Account:
    name: str
    asset: Asset

    balance_type: BalanceType
    balance: float

    def __init__(self, name: str, balance_type: BalanceType):
        self.name = name

        self.balance = 0.0
        self.balance_type = balance_type

    def debit(self, amount: float):
        if self.balance_type == BalanceType.DEBIT:
            self.balance += amount
        else:
            self.balance -= amount

    def credit(self, amount: float):
        if self.balance_type == BalanceType.DEBIT:
            self.balance -= amount
        else:
            self.balance += amount

from .accounting.account import Account


class User:
    name: str

    accounts: list[Account]

    def __init__(self, name: str):
        self.name = name

        self.accounts = []

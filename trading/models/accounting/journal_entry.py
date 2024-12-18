from .account import Account

from datetime import datetime
from enum import StrEnum, auto

class EntryType(StrEnum):
    DEBIT = auto()
    CREDIT = auto()


class Entry:
    account: Account
    entry_type: EntryType
    amount: float

    def __init__(self, account: Account, entry_type: EntryType, amount: float):
        self.account = account
        self.entry_type = entry_type
        self.amount = amount


class JournalEntry:
    date: datetime
    description: str

    entries: list[Entry]

    def __init__(self, description: str, date: datetime = datetime.now()):
        self.description = description
        self.date = date

    def add_entry(self, account: Account, entry_type: EntryType, amount: float):
        if entry_type not in [EntryType.DEBIT, EntryType.CREDIT]:
            raise ValueError("Entry type must be 'debit' or 'credit'")

        self.entries.append(Entry(account, entry_type, amount))

    def post(self):
        for entrie in self.entries:
            if entrie.entry_type == EntryType.DEBIT:
                entrie.account.debit(entrie.amount)
            elif entrie.entry_type == EntryType.CREDIT:
                entrie.account.credit(entrie.amount)



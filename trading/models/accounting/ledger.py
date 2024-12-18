from .journal_entry import JournalEntry

class Ledger:
    journal_entries: list[JournalEntry]

    def __init__(self):
        self.journal_entries = []

    def add_transaction(self, journal_entry: JournalEntry):
        journal_entry.post()
        self.journal_entries.append(journal_entry)

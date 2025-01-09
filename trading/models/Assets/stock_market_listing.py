from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.box import ROUNDED
from trading.models.money import Money

class Asset:
    def __init__(self, ticker_symbol, company_name, last_price : Money):
        self.ticker_symbol = ticker_symbol
        self.company_name = company_name
        self.bid_price = last_price
        self.ask_price = last_price
        self.last_price : Money = last_price

    def update_price(self, price : Money):
        self.last_price : Money = price

    def update_bid_price(self, price):
        self.bid_price = price

    def update_ask_price(self, price):
        self.ask_price = price

    def __str__(self):
        return f"Ticker: {self.ticker_symbol} Company: {self.company_name} Last Price: {self.last_price} Bid Price: {self.bid_price} Ask Price: {self.ask_price}"

    def visualize_ticker(self):
        """
        Visualizes the stock ticker with prices using rich styles and boxes.
        """
        console = Console()

        # Create the main title with ticker symbol
        title = f"[bold blue]{self.ticker_symbol} - {self.company_name}[/bold blue]"
        console.print(Panel(title, style="bold cyan", expand=True))

        # Create a table for the stock details (Last, Bid, Ask prices)
        table = Table(title=f"Stock Price Information for {self.ticker_symbol}", box=ROUNDED, title_style="bold green")
        table.add_column("Price Type", justify="left", style="yellow bold")
        table.add_column("Price", justify="right", style="magenta bold")

        # Add rows for Last, Bid, and Ask Prices
        table.add_row("Last Price", f"[bold green]{self.last_price.amount:.2f}[/bold green]")
        table.add_row("Bid Price", f"[bold red]{self.bid_price.amount:.2f}[/bold red]")
        table.add_row("Ask Price", f"[bold blue]{self.ask_price.amount:.2f}[/bold blue]")

        # Print the table
        console.print(table)

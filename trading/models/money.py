from decimal import Decimal, getcontext, ROUND_HALF_UP

class Money:
    """A class to represent money with high precision."""

    def __init__(self, amount, currency="CAD", precision=2):
        """
        Initialize the Money object.
        
        :param amount: The monetary value as a string or Decimal.
        :param currency: The currency of the money (default: "USD").
        :param precision: The number of decimal places to maintain (default: 2).
        """
        getcontext().prec = precision + 5  # Extra precision to handle operations
        self.amount = Decimal(amount).quantize(Decimal(f"1.{'0' * precision}"), rounding=ROUND_HALF_UP)
        self.currency = currency
        self.precision = precision

    def __repr__(self):
        return f"{self.amount} {self.currency}"

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add money of different currencies.")
        result = self.amount + other.amount
        return Money(result, self.currency, self.precision)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot subtract money of different currencies.")
        result = self.amount - other.amount
        return Money(result, self.currency, self.precision)

    def __mul__(self, factor):
        if not isinstance(factor, (int, Decimal, float)):
            raise TypeError("Multiplication only supports numeric types.")
        result = self.amount * Decimal(factor)
        return Money(result, self.currency, self.precision)

    def __truediv__(self, divisor):
        if not isinstance(divisor, (int, Decimal, float)):
            raise TypeError("Division only supports numeric types.")
        if divisor == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        result = self.amount / Decimal(divisor)
        return Money(result, self.currency, self.precision)

    def __eq__(self, other):
        if isinstance(other,Money):
            return self.amount == other.amount and self.currency == other.currency
        else:
            return float(self.amount) == float(other)

    def __lt__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot compare money of different currencies.")
        return self.amount < other.amount

    def __le__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot compare money of different currencies.")
        return self.amount <= other.amount

    def __gt__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot compare money of different currencies.")
        return self.amount > other.amount

    def __ge__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot compare money of different currencies.")
        return self.amount >= other.amount

    def __neg__(self):
        return Money(-self.amount, self.currency, self.precision)

    def to_string(self):
        """Returns a string representation of the money."""
        return f"{self.amount:.{self.precision}f} {self.currency}"

from __future__ import annotations
from enum import Enum
from decimal import Decimal
from dataclasses import dataclass
from src.base import EntityId
from src.accounting.src.domain.domain_exceptions import InvalidCurrencyException, InsufficientFundsException

@dataclass(frozen=True)
class AccountId(EntityId):
    pass
    
class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

@dataclass(frozen=True)
class MonetaryValue:
    amount: Decimal
    currency: str

    def __post_init__(self):
        # Validate amount
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        # Validate currency code 
        if len(self.currency) != 3:
            raise ValueError("Currency code must be 3 letters")
        # Ensure uppercase
        object.__setattr__(self, "currency", self.currency.upper())
    
    def __eq__(self, value):
        if not isinstance(value, MonetaryValue):
            return NotImplemented
        return self.amount == value.amount and self.currency == value.currency
    
    def __str__(self):
        return f"{self.amount} {self.currency}"

    #Side-effect free methods
    def add(self, other: MonetaryValue):
        """Add two MonetaryValue objects, returning a new MonetaryValue. Currencies must match."""
        if self.currency != other.currency:
            raise InvalidCurrencyException("Currency mismatch")
        return MonetaryValue(self.amount + other.amount, self.currency)

    def subtract(self, other: MonetaryValue):
        """Subtract one MonetaryValue from another, returning a new MonetaryValue. Currencies must match."""
        if self.currency != other.currency:
            raise InvalidCurrencyException("Currency mismatch")
        if self.amount < other.amount:
            raise InsufficientFundsException("Insufficient funds for this operation")
        return MonetaryValue(self.amount - other.amount, self.currency)
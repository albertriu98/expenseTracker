from src.base import EntityId
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4
from enum import Enum



class BudgetId(EntityId):
    pass

class CategoryId(EntityId):
    pass

@dataclass(frozen=True)
class MonetaryValue:
    _amount: Decimal
    _currency: str

    def __post_init__(self):
        # Validate amount
        if self._amount < 0:
            raise ValueError("Amount cannot be negative")
        # Validate currency code 
        if len(self._currency) != 3:
            raise ValueError("Currency code must be 3 letters")
        # Ensure uppercase
        object.__setattr__(self, "_currency", self._currency.upper())
    
    def __eq__(self, value):
        if not isinstance(value, MonetaryValue):
            return NotImplemented
        return self.amount == value.amount and self.currency == value.currency
    
    def __str__(self):
        return f"{self.amount} {self.currency}"
    
    @property
    def amount(self):
        return self._amount
    @property
    def currency(self):
        return self._currency

    #Side-effect free methods
    def add(self, other: MonetaryValue) -> MonetaryValue:
        if self._currency != other.currency:
            raise ValueError("Currency mismatch")
        return MonetaryValue(self._amount + other.amount, self._currency)

    def subtract(self, other: MonetaryValue) -> MonetaryValue:
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return MonetaryValue(self._amount - other.amount, self._currency)
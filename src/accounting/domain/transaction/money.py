from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Money:
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
    
    @property
    def amount(self):
        return self._amount
    @property
    def currency(self):
        return self._currency



from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"



from dataclasses import dataclass
from src.accounting.src.domain.value_objects import MonetaryValue
from src.base import Event

@dataclass(frozen=True)
class TransactionCommitted(Event):
    typeName = "TransactionCommitted"
    account_id: str
    money: MonetaryValue
    description: str
    transaction_type: str
    category_id: str = None

@dataclass(frozen=True)
class AccountCreated(Event):
    typeName = "AccountCreated"
    account_id: str
    initial_balance: MonetaryValue

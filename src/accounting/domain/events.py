from dataclasses import dataclass
from src.accounting.domain.value_objects import MonetaryValue, TransactionId
from src.base import Event



@dataclass(frozen=True)
class TransactionCommitted(Event):
    account_id: str
    money: MonetaryValue
    description: str
    transaction_type: str
    category_id: str = None

@dataclass(frozen=True)
class AccountCreated(Event):
    account_id: str
    initial_balance: MonetaryValue

@dataclass(frozen=True)
class categoryUpdated(Event):
    transactionId: TransactionId
    category_id: str
    new_category_name: str

@dataclass(frozen=True)
class TransferCommitted(Event):
    from_account_id: str
    to_account_id: str
    money: MonetaryValue
    description: str
    category_id: str = None
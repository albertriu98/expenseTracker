from dataclasses import dataclass
from src.accounting.domain.value_objects import Money

@dataclass(frozen=True)
class TransactionCommitted:
    account_id: str
    money: Money
    description: str
    transaction_type: str
    category_id: str = None

@dataclass(frozen=True)
class AccountCreated:
    account_id: str
    initial_balance: Money

@dataclass(frozen=True)
class categoryUpdated:
    category_id: str
    new_category_name: str

@dataclass(frozen=True)
class TransferCommitted:
    from_account_id: str
    to_account_id: str
    money: Money
    description: str
    category_id: str = None
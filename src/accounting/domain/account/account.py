from src.accounting.domain.accountId import AccountId
from src.accounting.domain.shared.domain_exceptions import InsufficientFundsException
from src.accounting.domain.money import Money
from src.accounting.domain.events import TransactionCommitted

class Account:
    def __init__(self, initBalance: decimal, currency: str):
        self._accountId = AccountId.new()
        self._currency = currency
        self._currentBalance = initBalance

    def deposit(self, amount: Money):
        if self._currency != amount.currency :
            raise InvalidCurrency("Transaction currency does not match with Account currency")
        self._current_balance += amount.amount
        
        return TransactionCommitted()

    def withdraw(self, amount : Money):
        if self._currentBalance < amount :
            raise InsufficientFundsException("Not enough balance to withdraw.")
        else if self._currency != amount.currency :
            raise InvalidCurrency("Transaction currency does not match with Account currency")
        self._currentBalance -= amount.amount
        return TransactionCommitted()

    @classmethod
    def openAccount(cls, initAmount: Money)
        return cls(Account(initBalance=initAmount.amount, currency=initAmount.currency))

    
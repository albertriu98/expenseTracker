from src.accounting.domain.account.accountId import AccountId
from src.accounting.domain.shared.domain_exceptions import InsufficientFundsException
from src.accounting.domain.account.money import Money
from src.accounting.domain.account.events import TransactionCommitted
from src.accounting.domain.transaction.transaction import Transaction

class Account:
    def __init__(self, initBalance: decimal, currency: str):
        self._accountId = AccountId.new()
        self._currency = currency
        self._currentBalance = initBalance
        self._dateCreated = datetime.now() #timestamp
        self._dateUpdated = datetime.now() #timestamp
    
    @property
    def accountId(self):
        return self._accountId
    
    @property
    def currency(self):
        return self._currency
    
    @property
    def currentBalance(self):
        return self._currentBalance

    @property
    def dateCreated(self):
        return self._dateCreated
    
    @property
    def dateUpdated(self):
        return self._dateUpdated

    def deposit(self, transaction: Transaction):
        if self._currency != transaction.currency :
            raise InvalidCurrency("Transaction currency does not match with Account currency")
        self._currentBalance += transaction.money.amount
        
        return TransactionCommitted(transaction_id=transaction.id, account_id=transaction.accountId, amount=transaction.amount,
                currency=transaction.currency, transaction_type=transaction.transactionType,  category_id=transaction.categoryId)

    def withdraw(self, transaction: Transaction):
        if self._currentBalance < transaction.amount :
            raise InsufficientFundsException("Not enough balance to withdraw.")
        elif self._currency != transaction.currency :
            raise InvalidCurrency("Transaction currency does not match with Account currency")
        self._currentBalance -= amount.amount
        return TransactionCommitted(transaction_id=transaction.id, account_id=transaction.accountId, amount=transaction.amount,
                currency=transaction.currency, transaction_type=transaction.transactionType,  category_id=transaction.categoryId)

    @classmethod
    def openAccount(cls, initAmount: Money)
        return cls(initBalance=initAmount.amount, currency=initAmount.currency)

    
from src.accounting.domain.value_objects import AccountId, MonetaryValue
from src.accounting.domain.events import TransactionCommitted, AccountCreated
from datetime import datetime, timezone
from src.base import AggregateRoot
from decimal import Decimal

class Account(AggregateRoot):
    _accountId: AccountId
    _currentBalance: MonetaryValue
    _dateCreated: datetime
    _dateUpdated: datetime
    _version: int
    
    def __init__(self, accountId: AccountId, aBalance: MonetaryValue, dateCreated: datetime, dateUpdated: datetime, version: int):
        super().__init__(version)
        self._accountId = accountId
        self._currentBalance = aBalance
        self._dateCreated = dateCreated
        self._dateUpdated = dateUpdated

    
    def __str__(self):
        return f"Account(id={self.accountId}, currentBalance={self.currentBalance}, currency='{self.currency}', dateCreated='{self.dateCreated}', dateUpdated='{self.dateUpdated}')"
    
    @property
    def accountId(self):
        return self._accountId
    
    @property
    def getCurrency(self):
        return self._currentBalance.currency
    
    @property
    def getCurrentBalance(self):
        return self._currentBalance.amount

    @property
    def dateCreated(self):
        return self._dateCreated
    
    @property
    def dateUpdated(self):
        return self._dateUpdated

    def deposit(self, money: MonetaryValue, description: str, categoryId: str):
        self._currentBalance = self._currentBalance.add(money) #Replace object
        self._dateUpdated = datetime.now(timezone.utc)
        self._version += 1
        self.add_event(TransactionCommitted(account_id=self._accountId, 
                                                money=money,
                                                transaction_type="income", 
                                                description=description, 
                                                category_id=categoryId,
                                                version=self._version))
        
    def withdraw(self, money: MonetaryValue, description: str, categoryId: str):
        self._currentBalance = self._currentBalance.subtract(money) #Replace object
        self._dateUpdated = datetime.now(timezone.utc)
        self._version += 1
        self.add_event(TransactionCommitted(account_id=self._accountId, 
                                                money=money,
                                                transaction_type="expense",  
                                                description=description,
                                                category_id=categoryId,
                                                version=self._version))

    @classmethod
    def create_account(cls, amount: Decimal, currency: str):
        return cls(AccountId.nextId(), MonetaryValue(amount, currency), datetime.now(timezone.utc), datetime.now(timezone.utc), 0)

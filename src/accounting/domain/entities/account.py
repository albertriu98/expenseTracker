from src.accounting.domain.value_objects import AccountId
from src.accounting.domain.domain_exceptions import InsufficientFundsException, InvalidCurrencyException
from src.accounting.domain.value_objects import Money
from src.accounting.domain.events import TransactionCommitted
from datetime import datetime
from src.base import AggregateRoot

class Account(AggregateRoot):
    def __init__(self, initBalance: Money):
        self._accountId = AccountId.new()
        self._currentBalance = initBalance
        self._dateCreated = datetime.now() #timestamp
        self._dateUpdated = datetime.now() #timestamp
        self._events = []
    
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

    def pull_events(self):
        events = self._events[:]
        self._events.clear()
        return events

    def deposit(self, money: Money, description: str, categoryId: str):
        if self._currentBalance.currency != money.currency :
            raise InvalidCurrencyException("Transaction currency does not match with Account currency")
        self._currentBalance = self._currentBalance.add(money)
        self._dateUpdated = datetime.now()
        self._events.append(TransactionCommitted(account_id=self.accountId, 
                                                money=money,
                                                transaction_type="income", 
                                                description=description, 
                                                category_id=categoryId))
        
    def withdraw(self, money: Money, description: str, categoryId: str):
        if self._currentBalance.amount < money.amount :
            raise InsufficientFundsException("Not enough balance to withdraw.")
        elif self._currentBalance.currency != money.currency :
            raise InvalidCurrencyException("Transaction currency does not match with Account currency")
        self._currentBalance = self._currentBalance.subtract(money)
        self._dateUpdated = datetime.now()
        self._events.append(TransactionCommitted(account_id=self.accountId, 
                                                money=money,
                                                transaction_type="expense",  
                                                description=description,
                                                category_id=categoryId))


    
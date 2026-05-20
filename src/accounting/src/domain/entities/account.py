from src.accounting.src.domain.value_objects import AccountId, MonetaryValue
from src.accounting.src.domain.events import TransactionCommitted, AccountCreated
from src.accounting.src.domain.domain_exceptions import InsufficientFundsException
from datetime import datetime, timezone
from src.base import AggregateRoot
from decimal import Decimal

class Account(AggregateRoot):
    _accountId: AccountId
    _currentBalance: MonetaryValue
    _dateCreated: datetime
    _dateUpdated: datetime
    _version: int
    
    def __init__(self, accountId: AccountId, userid: str, aBalance: MonetaryValue, dateCreated: datetime, dateUpdated: datetime, version: int, events: list = []):
        super().__init__(version, events)
        self._accountId = accountId
        self._userId = userid
        self._currentBalance = aBalance
        self._dateCreated = dateCreated
        self._dateUpdated = dateUpdated

    def __str__(self):
        return f"Account(id={self.accountId}, currentBalance={self.currentBalance}, currency='{self.currency}', dateCreated='{self.dateCreated}', dateUpdated='{self.dateUpdated}')"
    
    @property
    def accountId(self):
        return self._accountId
    
    @property
    def userid(self):
        return self._userId
    
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
        try:
            self._currentBalance = self._currentBalance.subtract(money) #Replace object
        except InsufficientFundsException as e:
            raise e
        self._dateUpdated = datetime.now(timezone.utc)
        self._version += 1
        self.add_event(TransactionCommitted(account_id=self._accountId, 
                                                money=money,
                                                transaction_type="expense",  
                                                description=description,
                                                category_id=categoryId,
                                                version=self._version))

    @classmethod
    def create_account(cls, amount: Decimal, currency: str, userid: str):
        account_id = AccountId.nextId()
        initial_balance = MonetaryValue(amount, currency)
        return cls(account_id, userid=userid, aBalance=initial_balance, dateCreated=datetime.now(timezone.utc), dateUpdated=datetime.now(timezone.utc), version=0, events=[AccountCreated(account_id=account_id, initial_balance=initial_balance, version=0)])

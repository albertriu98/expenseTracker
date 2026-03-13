from datetime import datetime
from uuid import UUID
from decimal import Decimal
from src.accounting.domain.value_objects import TransactionId
from src.accounting.domain.value_objects import TransactionType
from src.accounting.domain.value_objects import MonetaryValue
from src.accounting.domain.value_objects import AccountId
from src.accounting.domain.events import categoryUpdated
from src.base import AggregateRoot

class Transaction(AggregateRoot):
    def __init__(self, transactionType: TransactionType, accountId: AccountId, money: MonetaryValue,  description:  str, categoryId: str = ""):
        """Do not call this method directly to create new Transactions"""

        self._id = TransactionId.new()  # value object, immutable
        self._transactionType = transactionType #value object, immutable
        self.accountId = accountId #value object, immutable
        self._money = money #value object immutable
        self._description = description #attribute
        self._categoryId = categoryId #attribute
        self._dateCreated = datetime.now() #timestamp
        self._events = []

    def __str__(self):
        return f"Transaction(id={self.id}, transactionType='{self.transactionType}', amount={self.amount}, currency='{self.currency}', description='{self.description}', tag='{self.tag}')"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Transaction):
            return self.id == other.id
        return False
    
    @property
    def id(self):
        return self._id.value

    @property
    def transactionType(self):
        return self._transactionType
    
    @property
    def userId(self):
        return self._userId

    @property
    def amount(self):
        return self._money.amount
    
    @property
    def currency(self):
        return self._money.currency

    @property
    def description(self):
        return self._description
    
    @property
    def categoryId(self):
        return self._categoryId
    
    @property
    def dateCreated(self):
        return self._dateCreated
    
    @description.setter
    def description(self, newDescription: str):
        if self.description is None:
            raise ValueError("Description cannot be None")
        self._description = newDescription
        self._events.append(categoryUpdated(category_id=self.categoryId, new_category_name=newDescription, transactionId=self.id))

    @categoryId.setter
    def categoryId(self, newCategoryId: str):
        if self.categoryId is None:
            raise ValueError("Category ID cannot be None")
        self._categoryId = newCategoryId

    
    @classmethod
    def create_transaction(cls, transaction_type: str , account_id: UUID, amount: Decimal, currency: str, description: str, categoryId: str):
        return cls(TransactionType(transaction_type), AccountId(account_id), MonetaryValue(amount, currency), description, categoryId, )

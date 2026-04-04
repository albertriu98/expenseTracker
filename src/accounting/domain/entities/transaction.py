from datetime import datetime, timezone
from uuid import UUID
from decimal import Decimal
from src.accounting.domain.value_objects import TransactionId, TransactionType, MonetaryValue, AccountId
from src.accounting.domain.events import TransactionCategoryUpdated, TransactionDescriptionUpdated
from src.base import AggregateRoot

class Transaction(AggregateRoot):
    def __init__(self, transactionId: TransactionId, transactionType: TransactionType, accountId: AccountId, money: MonetaryValue,  adescription:  str, categoryId: str = "", version: int , dateCreated: datetime , dateUpdated: datetime):
        """Do not call this method directly to create new Transactions"""

        super().__init__(version)
        self._id = transactionId  # value object, immutable
        self._transactionType = transactionType #value object, immutable
        self.accountId = accountId #value object, immutable
        self._money = money #value object immutable
        self._description = adescription #attribute
        self._categoryId = categoryId #attribute
        self._dateCreated = dateCreated
        self._dateUpdated = dateUpdated

    def __str__(self):
        return f"Transaction(id={self.id}, transactionType='{self.transactionType.value}', amount={self.amount}, currency='{self.currency}', description='{self.description}', categoryId='{self.categoryId}')"

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
    
    @property
    def dateUpdated(self):
        return self._dateUpdated
    
    @description.setter
    def description(self, newDescription: str):
        if newDescription is None:
            raise ValueError("Description cannot be None")
        self._description = newDescription
        self._version += 1
        self._dateUpdated = datetime.now(timezone.utc)
        self._events.append(TransactionDescriptionUpdated(category_id=self.categoryId, 
                                                          new_description=newDescription, 
                                                          transactionId=self.id,
                                                          version=self._version))

    @categoryId.setter
    def categoryId(self, newCategoryId: str):
        if newCategoryId is None:
            raise ValueError("Category ID cannot be None")
        self._categoryId = newCategoryId
        self._version += 1
        self._dateUpdated = datetime.now(timezone.utc)
        self._events.append(TransactionCategoryUpdated(category_id=self.categoryId, 
                                            new_category_name=newCategoryId, 
                                            transactionId=self.id,
                                            version=self._version))

    
    @classmethod
    def create_transaction(cls, transaction_type: str , account_id: UUID, amount: Decimal, currency: str, description: str, categoryId: str):
       return cls(TransactionId.nextId(), TransactionType(transaction_type), AccountId(account_id), MonetaryValue(amount, currency), description, categoryId, 0, datetime.now(timezone.utc), datetime.now(timezone.utc))

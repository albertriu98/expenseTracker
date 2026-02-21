from datetime import datetime
from uuid import UUID
from decimal import Decimal
from src.accounting.domain.transaction.transactionId import TransactionId
from src.accounting.domain.transaction.transactionType import TransactionType
from src.accounting.domain.transaction.money import Money
from src.accounting.domain.transaction.description import Description
from src.accounting.domain.transaciton.accountId import AccountId


class Transaction:
    def __init__(self, transactionType: TransactionType, accountId: AccountId, money: Money,  description:  str, categoryId: str = ""):
        """Do not call this method directly to create new Transactions"""

        self._id = TransactionId.new()  # value object, immutable
        self._transactionType = transactionType #value object, immutable
        self.accountId = accountId #value object, immutable
        self._money = money #value object immutable
        self._description = description #attribute
        self._categoryId = categoryId #attribute
        self._dateCreated = datetime.now() #timestamp

    def __str__(self):
        return f"Transaction(id={self.id}, transactionType='{self.transactionType}', amount={self.amount}, currency='{self.currency}', description='{self.description}', tag='{self.tag}')"

    def __repr__(self):
        return self.__str__()
    
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
    
    @classmethod
    def create_transaction(cls, transaction_type: str , account_id: UUID, amount: Decimal, currency: str, description: str, categoryId: str = ""):
        return cls(TransactionType(transaction_type), UserId(user_id), Money(amount, currency), description, categoryId)

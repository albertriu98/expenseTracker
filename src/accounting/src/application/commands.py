from decimal import Decimal

class CreateAccountCommand:
    def __init__(self, amount, currency, userId):
        self._amount : Decimal = amount
        self._currency : str = currency
        self._userId : str = userId

    @property
    def amount(self):
        return self._amount
    
    @property
    def currency(self):
        return self._currency
    
    @property
    def userId(self):
        return self._userId

class CommitTransactionCommand:
    def __init__(self, accountId, amount, currency, description, category, transactionType):
        self._accountId : str = accountId
        self._amount : Decimal = amount
        self._currency : str = currency
        self._description : str = description
        self._category : str = category
        self._transactionType : str = transactionType

    @property
    def accountId(self):
        return self._accountId
    
    @property
    def amount(self):
        return self._amount
    
    @property
    def currency(self):
        return self._currency
    
    @property
    def description(self):
        return self._description
    
    @property
    def category(self):
        return self._category
    
    @property
    def transactionType(self):
        return self._transactionType
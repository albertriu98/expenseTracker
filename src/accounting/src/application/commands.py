from decimal import Decimal

class CreateAccountCommand:
    amount : Decimal
    currency : str

    def __init__(self, amount, currency):
        self._amount = amount
        self._currency = currency

    @property
    def amount(self):
        return self._amount
    
    @property
    def currency(self):
        return self._currency
    
class CommitTransactionCommand:
    _accountId: str
    _amount: Decimal
    _currency: str
    _description: str
    _category: str
    _transactionType: str

    def __init__(self, accountId, amount, currency, description, category, transactionType):
        self._accountId = accountId
        self._amount = amount
        self._currency = currency
        self._description = description
        self._category = category
        self._transactionType = transactionType

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
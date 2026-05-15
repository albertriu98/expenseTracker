from decimal import Decimal

class CreateAccountCommand:
    amount : Decimal
    currency : str

    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency
    
    @property
    def amount(self):
        return self.amount
    
    @property
    def currency(self):
        return self.currency
    
class CommitTransactionCommand:
    accountId: str
    amount: Decimal
    currency: str
    description: str
    category: str
    transactionType: str

    def __init__(self, accountId, amount, currency, description, category, transactionType):
        self.accountId = accountId
        self.amount = amount
        self.currency = currency
        self.description = description
        self.category = category
        self.transactionType = transactionType
    
    @property
    def accountId(self):
        return self.accountId
    
    @property
    def amount(self):
        return self.amount
    
    @property
    def currency(self):
        return self.currency
    
    @property
    def description(self):
        return self.description
    
    @property
    def category(self):
        return self.category
    
    @property
    def transactionType(self):
        return self.transactionType
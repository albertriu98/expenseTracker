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
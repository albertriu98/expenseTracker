class InsufficientFundsException(Exception):
    """Raised when an account does not have enough balance for a withdrawal."""
    pass

class InvalidCurrencyException(Expetion):
    """Raised when Account currency does not match transaction currency"""
    pass
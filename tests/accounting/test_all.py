import pytest
from uuid import uuid4
from decimal import Decimal
from src.accounting.domain.value_objects.money import Money
from src.accounting.domain.value_objects.transactionType import TransactionType
from src.accounting.domain.value_objects.description import Description
from src.accounting.domain.value_objects.userId import UserId
from src.accounting.domain.entities.transaction import Transaction

def test_transaction_creation():
    user_id = UserId(uuid4())
    transaction_type = TransactionType("income")
    money = Money(Decimal("100.00"), "USD")
    description = Description("Salary")
    tag = "Job"

    txn = Transaction(transaction_type, user_id, money, description, tag)

    assert txn.transactionType == transaction_type
    assert txn.userId == user_id
    assert txn.amount == Decimal("100.00")
    assert txn.currency == "USD"
    assert txn.description.text == "Salary"
    assert txn.tag == tag
    assert txn.id is not None
    assert txn.dateCreated is not None

def test_transaction_factory_from_primitives():
    user_id = uuid4()
    txn = Transaction.create_transaction(
        transaction_type="expense",
        user_id=user_id,
        amount=50.00,
        currency="USD",
        description="Groceries",
        tag="Food"
    )

    assert txn.transactionType.value == "expense"
    assert txn.userId.value == user_id
    assert txn.amount == Decimal("50.00")
    assert txn.currency == "USD"
    assert txn.description.text == "Groceries"
    assert txn.tag == "Food"

def test_invalid_transaction_type_raises():
    user_id = UserId(uuid4())
    money = Money(Decimal("10.00"), "USD")
    description = Description("Test")
    
    with pytest.raises(ValueError):
        Transaction(TransactionType("INVALID"), user_id, money, description)

def test_invalid_money_raises():
    with pytest.raises(ValueError):
        Money(Decimal("-5.00"), "USD")

def test_invalid_currency_raises():
    with pytest.raises(ValueError):
        Money(Decimal("10.00"), "US")  # Only 3-letter codes allowed

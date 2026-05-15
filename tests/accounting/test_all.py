import pytest
from decimal import Decimal
from uuid import UUID
from datetime import datetime, timezone

from src.accounting.src.domain.entities.account import Account
from src.accounting.src.domain.entities.transaction import Transaction
from src.accounting.src.domain.domain_exceptions import InsufficientFundsException, InvalidCurrencyException
from src.accounting.src.domain.events import AccountCreated, TransactionCommitted, TransactionCategoryUpdated, TransactionDescriptionUpdated
from src.accounting.src.domain.value_objects import MonetaryValue, TransactionType, AccountId, TransactionId
from src.base import EntityId


def test_monetary_value_creation_and_normalization():
    mv = MonetaryValue(Decimal("100.00"), "usd")

    assert mv.amount == Decimal("100.00")
    assert mv.currency == "USD"
    assert str(mv) == "100.00 USD"


def test_monetary_value_invalid_amount_raises():
    with pytest.raises(ValueError):
        MonetaryValue(Decimal("-1.00"), "USD")


def test_monetary_value_invalid_currency_length_raises():
    with pytest.raises(ValueError):
        MonetaryValue(Decimal("1.00"), "US")


def test_monetary_value_add_subtract_same_currency():
    mv = MonetaryValue(Decimal("100.00"), "USD")
    result_add = mv.add(MonetaryValue(Decimal("25.50"), "USD"))
    result_sub = mv.subtract(MonetaryValue(Decimal("20.00"), "USD"))

    assert result_add == MonetaryValue(Decimal("125.50"), "USD")
    assert result_sub == MonetaryValue(Decimal("80.00"), "USD")


def test_monetary_value_add_subtract_mismatched_currency_raises():
    mv = MonetaryValue(Decimal("100.00"), "USD")

    with pytest.raises(InvalidCurrencyException):
        mv.add(MonetaryValue(Decimal("10.00"), "EUR"))

    with pytest.raises(InvalidCurrencyException):
        mv.subtract(MonetaryValue(Decimal("10.00"), "EUR"))


def test_transaction_type_enum_values():
    assert TransactionType.INCOME.value == "income"
    assert TransactionType.EXPENSE.value == "expense"
    assert TransactionType("income") == TransactionType.INCOME
    assert TransactionType("expense") == TransactionType.EXPENSE

    with pytest.raises(ValueError):
        TransactionType("invalid")


def test_account_creation_initial_event_and_balance():
    account = Account.create_account(Decimal("200.00"), "CAD")

    assert account.getCurrentBalance == Decimal("200.00")
    assert account.getCurrency == "CAD"
    assert isinstance(account.accountId.value, UUID)

    events = account.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], AccountCreated)
    assert events[0].initial_balance == MonetaryValue(Decimal("200.00"), "CAD")

    assert account.pull_events() == []


def test_account_deposit_creates_transaction_event_and_updates_balance():
    account = Account.create_account(Decimal("100.00"), "USD")
    account.pull_events()  # clear initial event

    account.deposit(MonetaryValue(Decimal("50.00"), "USD"), "Paycheck", "salary")
    assert account.getCurrentBalance == Decimal("150.00")

    events = account.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], TransactionCommitted)
    assert events[0].transaction_type == "income"
    assert events[0].money == MonetaryValue(Decimal("50.00"), "USD")
    assert events[0].version == 1  # Should be the aggregate version after deposit


def test_account_event_store_contains_transaction_committed_after_deposit():
    account = Account.create_account(Decimal("100.00"), "USD")
    account.pull_events()  # clear initial AccountCreated event

    account.deposit(MonetaryValue(Decimal("25.00"), "USD"), "Side gig", "income")

    events = account.pull_events()
    assert any(isinstance(evt, TransactionCommitted) for evt in events)
    committed = [evt for evt in events if isinstance(evt, TransactionCommitted)]
    assert len(committed) == 1
    assert committed[0].money == MonetaryValue(Decimal("25.00"), "USD")


def test_account_withdraw_creates_transaction_event_and_updates_balance():
    account = Account.create_account(Decimal("100.00"), "USD")
    account.pull_events()  # clear initial event

    account.withdraw(MonetaryValue(Decimal("40.00"), "USD"), "Groceries", "food")
    assert account.getCurrentBalance == Decimal("60.00")

    events = account.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], TransactionCommitted)
    assert events[0].transaction_type == "expense"
    assert events[0].money == MonetaryValue(Decimal("40.00"), "USD")


def test_account_insufficient_funds_raises():
    account = Account.create_account(Decimal("10.00"), "USD")

    with pytest.raises(InsufficientFundsException):
        account.withdraw(MonetaryValue(Decimal("20.00"), "USD"), "Rent", "housing")


def test_account_invalid_currency_transaction_raises():
    account = Account.create_account(Decimal("100.00"), "USD")

    with pytest.raises(InvalidCurrencyException):
        account.deposit(MonetaryValue(Decimal("10.00"), "EUR"), "Transfer", "misc")

    with pytest.raises(InvalidCurrencyException):
        account.withdraw(MonetaryValue(Decimal("10.00"), "EUR"), "ATM", "cash")


def test_transaction_entity_basic_behaviour_and_category_update_event():
    account_id = AccountId.nextId()
    txn = Transaction.create_transaction("income", account_id.value, Decimal("25.00"), "USD", "Bonus", "salary")

    assert txn.transactionType == TransactionType.INCOME
    assert txn.accountId == account_id
    assert txn.amount == Decimal("25.00")
    assert txn.currency == "USD"
    assert txn.description == "Bonus"
    assert txn.categoryId == "salary"

    other = Transaction.create_transaction("expense", account_id.value, Decimal("1.00"), "USD", "Test", "misc")
    assert txn != other
    assert txn == txn

    txn.categoryId = "tax"
    assert txn.categoryId == "tax"
    assert len(txn._events) == 1
    assert isinstance(txn._events[0], TransactionCategoryUpdated)
    assert txn._events[0].new_category_name == "tax"


# Tests for EntityId and derived classes
def test_entity_id_creation():
    entity_id = EntityId.nextId()
    assert isinstance(entity_id.value, UUID)


def test_transaction_id_creation():
    txn_id = TransactionId.nextId()
    assert isinstance(txn_id.value, UUID)


def test_account_id_creation():
    acc_id = AccountId.nextId()
    assert isinstance(acc_id.value, UUID)


# Tests for Events
def test_account_created_event():
    mv = MonetaryValue(Decimal("100.00"), "USD")
    event = AccountCreated(account_id="test_id", initial_balance=mv, version=0)
    assert event.typeName == "AccountCreated"
    assert event.account_id == "test_id"
    assert event.initial_balance == mv
    assert event.version == 0


def test_transaction_committed_event():
    mv = MonetaryValue(Decimal("50.00"), "USD")
    event = TransactionCommitted(account_id="acc_id", money=mv, description="test", transaction_type="income", category_id="salary", version=0)
    assert event.typeName == "TransactionCommitted"
    assert event.account_id == "acc_id"
    assert event.money == mv
    assert event.description == "test"
    assert event.transaction_type == "income"
    assert event.category_id == "salary"
    assert event.version == 0


def test_transaction_category_updated_event():
    txn_id = TransactionId.nextId()
    event = TransactionCategoryUpdated(transactionId=txn_id, category_id="old_cat", new_category_name="new_cat", version=0)
    assert event.typeName == "TransactionCategoryUpdated"
    assert event.transactionId == txn_id
    assert event.category_id == "old_cat"
    assert event.new_category_name == "new_cat"
    assert event.version == 0


def test_transaction_description_updated_event():
    txn_id = TransactionId.nextId()
    event = TransactionDescriptionUpdated(transactionId=txn_id, category_id="cat", new_description="new desc", version=0)
    assert event.typeName == "TransactionDescriptionUpdated"
    assert event.transactionId == txn_id
    assert event.category_id == "cat"
    assert event.new_description == "new desc"
    assert event.version == 0


def test_event_to_dict():
    mv = MonetaryValue(Decimal("100.00"), "USD")
    event = AccountCreated(account_id="test_id", initial_balance=mv, version=0)
    data = event.to_dict()
    assert "account_id" in data['payload']
    assert "initial_balance" in data['payload']
    assert "version" in data['payload']
    assert "eventType" in data


# Tests for AggregateRoot
def test_aggregate_root_events():
    account = Account.create_account(Decimal("100.00"), "USD")
    events = account.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], AccountCreated)
    # After pulling, events should be cleared
    assert account.pull_events() == []


# Additional Account tests
def test_account_create_account_classmethod():
    account = Account.create_account(Decimal("150.00"), "EUR")
    assert account.getCurrentBalance == Decimal("150.00")
    assert account.getCurrency == "EUR"


def test_account_version_increment_on_operations():
    account = Account.create_account(Decimal("100.00"), "USD")
    initial_version = account._version
    account.pull_events()  # clear events
    account.deposit(MonetaryValue(Decimal("10.00"), "USD"), "test", "misc")
    assert account._version == initial_version + 1


def test_account_date_updated_on_operations():
    account = Account.create_account(Decimal("100.00"), "USD")
    initial_date = account.dateUpdated
    account.deposit(MonetaryValue(Decimal("10.00"), "USD"), "test", "misc")
    assert account.dateUpdated > initial_date


# Additional Transaction tests
def test_transaction_create_transaction_classmethod():
    acc_id = AccountId.nextId()
    txn = Transaction.create_transaction("income", acc_id.value, Decimal("25.00"), "USD", "Bonus", "salary")
    assert txn.transactionType == TransactionType.INCOME
    assert txn.accountId == acc_id
    assert txn.amount == Decimal("25.00")
    assert txn.currency == "USD"
    assert txn.description == "Bonus"
    assert txn.categoryId == "salary"


def test_transaction_description_setter():
    acc_id = AccountId.nextId()
    txn = Transaction.create_transaction("expense", acc_id.value, Decimal("10.00"), "USD", "Old desc", "misc")
    txn.description = "New desc"
    assert txn.description == "New desc"
    assert len(txn._events) == 1
    assert isinstance(txn._events[0], TransactionDescriptionUpdated)
    assert txn._events[0].new_description == "New desc"


def test_transaction_category_id_setter():
    acc_id = AccountId.nextId()
    txn = Transaction.create_transaction("expense", acc_id.value, Decimal("10.00"), "USD", "Test", "old_cat")
    txn.categoryId = "new_cat"
    assert txn.categoryId == "new_cat"
    assert len(txn._events) == 1
    assert isinstance(txn._events[0], TransactionCategoryUpdated)
    assert txn._events[0].new_category_name == "new_cat"


def test_transaction_equality():
    acc_id = AccountId.nextId()
    txn1 = Transaction.create_transaction("income", acc_id.value, Decimal("10.00"), "USD", "Test", "misc")
    txn2 = Transaction.create_transaction("income", acc_id.value, Decimal("10.00"), "USD", "Test", "misc")
    txn3 = Transaction.create_transaction("expense", acc_id.value, Decimal("10.00"), "USD", "Test", "misc")

    assert txn1 == txn1
    assert txn1 != txn2  # Different IDs
    assert txn1 != txn3  # Different IDs
    assert txn1 != "not a transaction"


def test_transaction_str_representation():
    acc_id = AccountId.nextId()
    txn = Transaction.create_transaction("income", acc_id.value, Decimal("25.00"), "USD", "Bonus", "salary")
    str_repr = str(txn)
    assert "Transaction" in str_repr
    assert "income" in str_repr
    assert "25.00" in str_repr
    assert "USD" in str_repr


def test_transaction_properties():
    acc_id = AccountId.nextId()
    txn = Transaction.create_transaction("expense", acc_id.value, Decimal("30.00"), "EUR", "Groceries", "food")

    assert txn.transactionType == TransactionType.EXPENSE
    assert txn.accountId == acc_id
    assert txn.amount == Decimal("30.00")
    assert txn.currency == "EUR"
    assert txn.description == "Groceries"
    assert txn.categoryId == "food"
    assert isinstance(txn.dateCreated, datetime)
    assert isinstance(txn.id, UUID)


# Tests for domain exceptions
def test_insufficient_funds_exception():
    exc = InsufficientFundsException("Test message")
    assert str(exc) == "Test message"


def test_invalid_currency_exception():
    exc = InvalidCurrencyException("Currency mismatch")
    assert str(exc) == "Currency mismatch"


# Additional MonetaryValue tests
def test_monetary_value_equality():
    mv1 = MonetaryValue(Decimal("100.00"), "USD")
    mv2 = MonetaryValue(Decimal("100.00"), "USD")
    mv3 = MonetaryValue(Decimal("100.00"), "EUR")
    mv4 = MonetaryValue(Decimal("50.00"), "USD")

    assert mv1 == mv2
    assert mv1 != mv3
    assert mv1 != mv4
    assert mv1 != "not monetary value"


def test_monetary_value_subtract_insufficient_funds():
    mv = MonetaryValue(Decimal("10.00"), "USD")
    with pytest.raises(InsufficientFundsException):
        mv.subtract(MonetaryValue(Decimal("20.00"), "USD"))

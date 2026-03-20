import pytest
from decimal import Decimal
from uuid import UUID

from src.accounting.domain.entities.account import Account
from src.accounting.domain.entities.transaction import Transaction
from src.accounting.domain.domain_exceptions import InsufficientFundsException, InvalidCurrencyException
from src.accounting.domain.events import AccountCreated, TransactionCommitted, categoryUpdated
from src.accounting.domain.value_objects import MonetaryValue, TransactionType, AccountId


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

    with pytest.raises(ValueError):
        mv.add(MonetaryValue(Decimal("10.00"), "EUR"))

    with pytest.raises(ValueError):
        mv.subtract(MonetaryValue(Decimal("10.00"), "EUR"))


def test_transaction_type_enum_values():
    assert TransactionType.INCOME.value == "income"
    assert TransactionType.EXPENSE.value == "expense"
    assert TransactionType("income") == TransactionType.INCOME
    assert TransactionType("expense") == TransactionType.EXPENSE

    with pytest.raises(ValueError):
        TransactionType("invalid")


def test_account_creation_initial_event_and_balance():
    account = Account(MonetaryValue(Decimal("200.00"), "CAD"))

    assert account.getCurrentBalance == Decimal("200.00")
    assert account.getCurrency == "CAD"
    assert isinstance(account.accountId.value, UUID)

    events = account.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], AccountCreated)
    assert events[0].initial_balance == MonetaryValue(Decimal("200.00"), "CAD")

    assert account.pull_events() == []


def test_account_deposit_creates_transaction_event_and_updates_balance():
    account = Account(MonetaryValue(Decimal("100.00"), "USD"))
    account.pull_events()  # clear initial event

    account.deposit(MonetaryValue(Decimal("50.00"), "USD"), "Paycheck", "salary")
    assert account.getCurrentBalance == Decimal("150.00")

    events = account.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], TransactionCommitted)
    assert events[0].transaction_type == "income"
    assert events[0].money == MonetaryValue(Decimal("50.00"), "USD")


def test_account_event_store_contains_transaction_committed_after_deposit():
    account = Account(MonetaryValue(Decimal("100.00"), "USD"))
    account.pull_events()  # clear initial AccountCreated event

    account.deposit(MonetaryValue(Decimal("25.00"), "USD"), "Side gig", "income")

    events = account.pull_events()
    assert any(isinstance(evt, TransactionCommitted) for evt in events)
    committed = [evt for evt in events if isinstance(evt, TransactionCommitted)]
    assert len(committed) == 1
    assert committed[0].money == MonetaryValue(Decimal("25.00"), "USD")


def test_account_withdraw_creates_transaction_event_and_updates_balance():
    account = Account(MonetaryValue(Decimal("100.00"), "USD"))
    account.pull_events()  # clear initial event

    account.withdraw(MonetaryValue(Decimal("40.00"), "USD"), "Groceries", "food")
    assert account.getCurrentBalance == Decimal("60.00")

    events = account.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], TransactionCommitted)
    assert events[0].transaction_type == "expense"
    assert events[0].money == MonetaryValue(Decimal("40.00"), "USD")


def test_account_insufficient_funds_raises():
    account = Account(MonetaryValue(Decimal("10.00"), "USD"))

    with pytest.raises(InsufficientFundsException):
        account.withdraw(MonetaryValue(Decimal("20.00"), "USD"), "Rent", "housing")


def test_account_invalid_currency_transaction_raises():
    account = Account(MonetaryValue(Decimal("100.00"), "USD"))

    with pytest.raises(InvalidCurrencyException):
        account.deposit(MonetaryValue(Decimal("10.00"), "EUR"), "Transfer", "misc")

    with pytest.raises(InvalidCurrencyException):
        account.withdraw(MonetaryValue(Decimal("10.00"), "EUR"), "ATM", "cash")


def test_transaction_entity_basic_behaviour_and_category_update_event():
    account_id = AccountId.new()
    txn = Transaction(TransactionType.INCOME, account_id, MonetaryValue(Decimal("25.00"), "USD"), "Bonus", "salary")

    assert txn.transactionType == TransactionType.INCOME
    assert txn.accountId == account_id
    assert txn.amount == Decimal("25.00")
    assert txn.currency == "USD"
    assert txn.description == "Bonus"
    assert txn.categoryId == "salary"

    original_id = txn.id
    other = Transaction(TransactionType.EXPENSE, account_id, MonetaryValue(Decimal("1.00"), "USD"), "Test", "misc")
    assert txn != other
    assert txn == txn

    txn.categoryId = "tax"
    assert txn.categoryId == "tax"
    assert len(txn._events) == 1
    assert isinstance(txn._events[0], categoryUpdated)
    assert txn._events[0].new_category_name == "tax"


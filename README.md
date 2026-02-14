# Expense Tracker

A Python-based expense tracking application built with **Domain Driven Design (DDD)** principles to manage personal finances through transactions and budgets.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Domain Model](#domain-model)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Implementation Status](#implementation-status)
- [Technologies](#technologies)

## Overview

Expense Tracker is designed to help users manage their personal finances by:
- Creating and managing customer accounts with secure authentication
- Recording income and expense transactions
- Organizing transactions with tags and categories
- Managing budgets for expense control

The project emphasizes clean architecture through Domain Driven Design, separating domain logic from infrastructure concerns.

## Architecture

This project follows **Domain Driven Design (DDD)** principles with clear separation of concerns:

```
src/
├── accounting/          # Accounting bounded context
│   └── domain/
│       ├── aggregates/  # Aggregate roots
│       ├── entities/    # Domain entities
│       └── value_objects/ # Immutable value objects
└── identity/            # Identity bounded context
    └── domain/
        ├── entities/    # Domain entities
        └── value_objects/ # Immutable value objects
```

### Bounded Contexts
- **Identity Context**: Manages customer registration, authentication, and user credentials
- **Accounting Context**: Manages transactions and budgets for expense tracking

## Project Structure

```
expenseTracker/
├── src/
│   ├── accounting/
│   │   └── domain/
│   │       ├── aggregates/
│   │       │   └── account.py          # Account aggregate (WIP)
│   │       ├── entities/
│   │       │   ├── budget.py           # Budget entity (WIP)
│   │       │   └── transaction.py      # Transaction entity
│   │       └── value_objects/
│   │           ├── description.py      # Transaction description
│   │           ├── money.py            # Money value object with amount & currency
│   │           ├── transactionId.py    # Unique transaction identifier
│   │           ├── transactionType.py  # Income/Expense type
│   │           └── userId.py           # User identifier reference
│   └── identity/
│       └── domain/
│           ├── entities/
│           │   └── customer.py         # Customer entity
│           └── value_objects/
│               ├── email.py            # Email with validation
│               ├── password.py         # Password with validation
│               └── userId.py           # Unique user identifier
├── tests/
│   └── accounting/
│       └── test_all.py                 # Unit tests
├── requirements.txt
└── README.md
```

## Domain Model

### Entities

#### **Customer** (`identity/domain/entities/customer.py`)
Represents a registered user in the system.

**Properties:**
- `id` (UserId): Unique customer identifier (UUID)
- `name` (str): Customer's full name
- `email` (Email): Customer's email address (validated)
- `password` (Password): Customer's password (encrypted/hashed)

**Factory Method:**
```python
Customer.create(name: str, email: str, password: str) -> Customer
```

#### **Transaction** (`accounting/domain/entities/transaction.py`)
Represents a financial transaction (income or expense).

**Properties:**
- `id` (TransactionId): Unique transaction identifier (UUID)
- `transactionType` (TransactionType): Either INCOME or EXPENSE
- `userId` (UserId): Reference to the customer who created this transaction
- `amount` (Decimal): Transaction amount
- `currency` (str): 3-letter ISO currency code (e.g., USD, EUR)
- `description` (Description): What the transaction is for
- `tag` (str): Category/tag for filtering transactions
- `dateCreated` (datetime): When the transaction was created

**Factory Method:**
```python
Transaction.create_transaction(
    transaction_type: str,
    user_id: UUID,
    amount: Decimal,
    currency: str,
    description: str,
    tag: str = ""
) -> Transaction
```

#### **Budget** (`accounting/domain/entities/budget.py`)
*(Currently in development)*

Will represent spending limits for budget categories.

### Value Objects

Value objects are immutable objects that represent specific concepts with validation:

#### **Email** (`identity/domain/value_objects/email.py`)
- Validates email format using regex
- **Properties:** `value`
- **Factory Method:** `Email.from_text(email_str: str)`
- **Method:** `update(new_email: str)` - Returns new Email instance

#### **Password** (`identity/domain/value_objects/password.py`)
- Validates password strength: minimum 8 characters with letters and digits
- **Properties:** `value`
- **Factory Method:** `Password.from_text(password_str: str)`
- **Method:** `update(new_password: str)` - Returns new Password instance

#### **Money** (`accounting/domain/value_objects/money.py`)
Immutable representation of monetary value.
- **Properties:** 
  - `amount` (Decimal): Must be non-negative
  - `currency` (str): Must be exactly 3 uppercase letters
- **Validation:** Amount cannot be negative, currency code format enforced

#### **TransactionType** (`accounting/domain/value_objects/transactionType.py`)
Enumeration with two possible values:
- `INCOME = "income"`
- `EXPENSE = "expense"`

#### **Description** (`accounting/domain/value_objects/description.py`)
Immutable text description of a transaction.
- **Properties:** `text`

#### **TransactionId** (`accounting/domain/value_objects/transactionId.py`)
Unique identifier for transactions.
- **Factory Method:** `TransactionId.new()` - Generates UUID-based ID
- **Properties:** `value`

#### **UserId** (`identity/domain/value_objects/userId.py`)
Unique identifier for customers.
- **Factory Method:** `UserId.new()` - Generates UUID-based ID
- **Properties:** `value`

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd expenseTracker
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

Execute the test suite using pytest:

```bash
pytest
```

Or run tests with verbose output:

```bash
pytest -v
```

### Test Coverage

Current test file: `tests/accounting/test_all.py`

Tests validate:
- Transaction creation with domain entities
- Transaction factory method from primitives
- Invalid transaction type validation
- Invalid money values validation
- Currency code validation

## Implementation Status

### ✅ Completed
- **Value Objects:** Email, Password, Money, TransactionType, Description, TransactionId, UserId
- **Entities:** Customer, Transaction
- **Unit Tests:** Transaction and Money validation tests
- **Domain Logic:** Validation and factory methods

### 🚧 In Progress / TODO
- **Budget Entity:** Definition and implementation
- **Account Aggregate:** Root aggregate for customer accounts
- **API Layer (FastAPI):** REST endpoints for all operations
- **Application Layer:** Use cases and commands
- **Infrastructure Layer:** PostgreSQL persistence and repositories
- **Authentication:** Password hashing and JWT tokens
- **Customer Operations:** Register, update email, update password
- **Transaction Operations:** Create, update, delete, query
- **Budget Operations:** Create, update, delete, check limits
- **Integration Tests:** End-to-end testing

## Technologies

- **Python 3.8+** - Core language
- **FastAPI** - Web framework (planned)
- **PostgreSQL** - Database (planned)
- **pytest** - Testing framework
- **Dataclasses** - Value object implementation

## Domain-Driven Design Principles Used

1. **Ubiquitous Language:** Clear domain terminology (Transaction, Customer, Money, etc.)
2. **Value Objects:** Immutable, validated objects like Money, Email, Password
3. **Entities:** Mutable objects with identity (Customer, Transaction)
4. **Aggregates:** Grouping of related entities (Account aggregate planned)
5. **Factory Methods:** Clean creation of domain objects with validation
6. **Validation:** Domain rules enforced at the value object and entity level

## Future Enhancements

- [ ] Implement Account aggregate root
- [ ] Build REST API with FastAPI
- [ ] Implement repository pattern for persistence
- [ ] Add customer use cases (register, login, manage profile)
- [ ] Add transaction use cases (create, update, delete, filter)
- [ ] Add budget management
- [ ] Implement proper authentication and authorization
- [ ] Add database migrations
- [ ] Create API documentation with Swagger/OpenAPI
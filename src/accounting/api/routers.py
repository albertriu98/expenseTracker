from fastapi import APIRouter, HTTPException
from typing import List
from src.accounting.application.services import AccountHandler
from src.accounting.application.commands import CreateAccountCommand, CommitTransactionCommand


router = APIRouter(
    prefix="/accounting",
    tags=["accounting"],
    responses={404: {"description": "Not found"}},
)

account_handler = AccountHandler()  # You would typically inject dependencies here

@router.get("/create_account", response_model=List[str])
async def create_account(amount: float, currency: str):
    # Placeholder implementation for creating an account
    account_id = account_handler.create_account(CreateAccountCommand(amount=amount, currency=currency))
    return ["Account created successfully"]

@router.post("/commit_transaction")
async def commit_transaction():
    # Placeholder implementation for committing a transaction
    current_balance = account_handler.commit_transaction()
    return {"message": "Transaction committed successfully", "current_balance": current_balance}
from fastapi import APIRouter, Depends
from typing import List
from src.accounting.src.application.services import AccountHandler
from src.accounting.src.application.commands import CreateAccountCommand, CommitTransactionCommand
from src.accounting.src.infrastructure.database.session import get_session
from sqlmodel import Session


router = APIRouter(
    prefix="/accounting",
    tags=["accounting"],
    responses={404: {"description": "Not found"}},
)

def get_handler(session: Session = Depends(get_session)):
    return AccountHandler(session)

@router.post("/create_account")
async def create_account(amount: float, currency: str, handler: AccountHandler = Depends(get_handler)):
    account_id = handler.create_account(CreateAccountCommand(amount=amount, currency=currency))
    return {"accountId": account_id}


@router.post("/commit_transaction")
async def commit_transaction(accountId: str, amount: float, currency: str, description: str, category: str, transactionType: str, handler: AccountHandler = Depends(get_handler)):
    current_balance = handler.commit_transaction(CommitTransactionCommand(
        account_id=accountId,
        amount=amount,
        currency=currency,
        description=description,
        category=category,
        transaction_type=transactionType
    ))

    return {"currentBalance": current_balance}

from fastapi import APIRouter, Depends, HTTPException
from src.accounting.src.application.services import AccountHandler
from src.accounting.src.application.commands import CreateAccountCommand, CommitTransactionCommand
from src.accounting.src.infrastructure.database.session import get_session
from src.accounting.src.domain.domain_exceptions import InsufficientFundsException
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
    try:
        current_balance = handler.commit_transaction(CommitTransactionCommand(
            accountId=accountId,
            amount=amount,
            currency=currency,
            description=description,
            category=category,
            transactionType=transactionType
        ))
        return {"currentBalance": current_balance}
    except InsufficientFundsException as e:
        raise HTTPException(status_code=400, detail=str(e))
        
from src.accounting.domain.entities.account import Account

class AccountRepository:
    def get_account(self, account_id: str) -> Account:
        raise NotImplementedError

    def save_account(self, account: Account) -> None:
        raise NotImplementedError
    
    def delete_account(self, account_id: str) -> None:
        raise NotImplementedError
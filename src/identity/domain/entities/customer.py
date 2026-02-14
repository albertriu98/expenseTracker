from src.identity.domain.value_objects.email import Email
from src.identity.domain.value_objects.password import Password
from src.identity.domain.value_objects.userId import UserId

class Customer:
    def __init__(self, name: str, email: Email, password: Password):
        """Do not use this constructor directly. Use the factory method `create` instead."""
        self._id = UserId.new()
        self._name = name
        self._email = email
        self._password = password
    
    def __str__(self):
        return f"Customer(id={self.id}, name='{self.name}', email='{self.email}')"
    
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def email(self):
        return self._email
    @property
    def password(self):
        return self._password
    
    @classmethod
    def register_customer(cls, name: str, email: str, password: str):
        email_vo = Email.from_text(email)
        password_vo = Password(password)
        return cls(name, email_vo, password_vo)
    

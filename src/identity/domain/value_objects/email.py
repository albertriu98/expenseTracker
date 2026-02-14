from dataclasses import dataclass

@dataclass
class Email:
    value: str

    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise ValueError(f"Invalid email address: {self.value}")

    @classmethod
    def from_text(cls, email_str: str):
        return cls(email_str)

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        # Simple regex for validating an email address
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    @property
    def value(self):
        return self._value
    
    def update(self, new_email: str):
        if not self._is_valid_email(new_email):
            raise ValueError(f"Invalid email address: {new_email}")
        return Email(new_email)
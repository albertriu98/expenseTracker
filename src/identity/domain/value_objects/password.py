from dataclasses import dataclass

@dataclass
class Password:
    value: str

    def __post_init__(self):
        if not self._is_valid_password(self.value):
            raise ValueError("Password must be at least 8 characters long and contain a mix of letters and numbers.")

    @classmethod
    def from_text(cls, password_str: str):
        return cls(password_str)

    @staticmethod
    def _is_valid_password(password: str) -> bool:
        if len(password) < 8:
            return False
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        return has_letter and has_digit
    
    @property
    def value(self):
        return self._value
    
    def update(self, new_password: str):
        if not self._is_valid_password(new_password):
            raise ValueError("Password must be at least 8 characters long and contain a mix of letters and numbers.")
        return Password(new_password)
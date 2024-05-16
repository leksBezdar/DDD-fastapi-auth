from dataclasses import dataclass
from email_validator import validate_email, EmailNotValidError

from domain.exceptions.users import (
    EmptyEmail,
    EmptyGroupTitle,
    EmptyPassword,
    EmptyUsername,
    GroupTitleTooLong,
    PasswordLengthIsNotValid,
    UsernameTooLong,
)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Username(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            return EmptyUsername()

        if len(self.value) > 15:
            raise UsernameTooLong(self.value)

    def as_generic_type(self):
        return str(self.value)
    
@dataclass(frozen=True)
class Email(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            return EmptyEmail()
        
        validate_email(self.value, check_deliverability=False)
    
    def as_generic_type(self):
        return str(self.value)

@dataclass(frozen=True)
class Password(BaseValueObject):
    value: str
    
    def validate(self):
        if not self.value:
            return EmptyPassword()
        
        if 3 <= len(self.value) <= 15:
            raise PasswordLengthIsNotValid(self.value)

@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            return EmptyGroupTitle()

        if len(self.value) > 15:
            raise GroupTitleTooLong(self.value)

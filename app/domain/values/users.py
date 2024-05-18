from dataclasses import dataclass
from email_validator import validate_email

from domain.exceptions.users import (
    EmptyEmail,
    EmptyGroupTitle,
    EmptyPassword,
    EmptyUsername,
    GroupTitleTooLong,
    PasswordLengthIsNotValid,
    UsernameLengthIsNotValid,
)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Username(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyUsername()

        value_length = len(self.value)

        if value_length not in range(3, 16):
            raise UsernameLengthIsNotValid(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Email(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyEmail()

        validate_email(self.value, check_deliverability=False)

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class Password(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyPassword()

        value_length = len(self.value)

        if value_length not in range(3, 16):
            raise PasswordLengthIsNotValid(self.value)

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyGroupTitle()

        if len(self.value) > 15:
            raise GroupTitleTooLong(self.value)

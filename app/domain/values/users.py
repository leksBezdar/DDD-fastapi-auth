from dataclasses import dataclass
import re
from typing import Self
import bcrypt

from domain.exceptions.users import (
    EmptyEmail,
    EmptyPassword,
    EmptyUsername,
    InvalidEmail,
    PasswordLengthIsNotValid,
    UsernameLengthIsNotValid,
)
from domain.values.base import BaseValueObject


@dataclass
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


@dataclass
class Email(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyEmail()

        email_validate_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_validate_pattern, self.value):
            raise InvalidEmail(self.value)

    def as_generic_type(self):
        return str(self.value)


@dataclass
class Password(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyPassword()

        value_length = len(self.value)

        if value_length not in range(3, 16):
            raise PasswordLengthIsNotValid(value_length)

    def as_generic_type(self):
        return str(self.value)

    def as_hash(self) -> Self:
        self.value = bcrypt.hashpw(self.value.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )
        return self

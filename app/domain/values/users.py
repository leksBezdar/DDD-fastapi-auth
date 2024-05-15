from dataclasses import dataclass

from domain.exceptions.users import (
    EmptyGroupTitle,
    EmptyUsername,
    GroupTitleTooLong,
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
class Title(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            return EmptyGroupTitle()

        if len(self.value) > 15:
            raise GroupTitleTooLong(self.value)

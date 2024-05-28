from dataclasses import dataclass

from domain.exceptions.groups import (
    EmptyGroupTitle,
    GroupTitleLengthIsNotValid,
)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyGroupTitle()

        if len(self.value) not in range(3, 16):
            raise GroupTitleLengthIsNotValid(self.value)

    def as_generic_type(self):
        return str(self.value)

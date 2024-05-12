from dataclasses import dataclass

from domain.exceptions.users import EmptyUsername, UsernameTooLong
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Username(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            return EmptyUsername(self.value)

        if len(self.value) > 15:
            raise UsernameTooLong(self.value)

    def as_generic_type(self):
        return str(self.value)

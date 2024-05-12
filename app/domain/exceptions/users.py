from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class UsernameTooLong(ApplicationException):
    username_value: str

    @property
    def message(self):
        return f"Username is too long: {self.username_value}"


@dataclass(eq=False)
class EmptyUsername(ApplicationException):
    username_value: str

    @property
    def message(self):
        return f"Username is empty: {self.username_value}"

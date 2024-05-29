from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class UsernameLengthIsNotValid(ApplicationException):
    username_value: str

    @property
    def message(self) -> str:
        return f"Username length is not valid: {self.username_value}"


@dataclass(eq=False)
class EmptyUsername(ApplicationException):
    @property
    def message(self) -> str:
        return "Username is empty"


@dataclass(eq=False)
class EmptyPassword(ApplicationException):
    @property
    def message(self) -> str:
        return "Password is empty"


@dataclass(eq=False)
class PasswordLengthIsNotValid(ApplicationException):
    length: str

    @property
    def message(self) -> str:
        return f"Password length is not valid: {self.length}"


@dataclass(eq=False)
class EmptyEmail(ApplicationException):
    @property
    def message(self) -> str:
        return "Email is empty"


@dataclass(eq=False)
class InvalidEmail(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f"The provided email is not valid: {self.email}"

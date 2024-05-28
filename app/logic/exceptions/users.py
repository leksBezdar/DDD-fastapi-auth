from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class UserAlreadyExistsException(LogicException):
    @property
    def message(self):
        return "User already exists"


@dataclass(eq=False)
class UserNotFoundException(LogicException):
    oid: str

    @property
    def message(self):
        return f"User with {self.oid=} was not found"


@dataclass(eq=False)
class TokenNotFoundException(LogicException):
    @property
    def message(self):
        return "Token was not found"


@dataclass(eq=False)
class InvalidCredentialsException(LogicException):
    @property
    def message(self):
        return "Invalid credentials were provided"

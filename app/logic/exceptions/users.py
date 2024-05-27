from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class GroupAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f"Group with that title already exists: {self.title}"


@dataclass(eq=False)
class UserAlreadyExistsException(LogicException):
    @property
    def message(self):
        return "User already exists"


@dataclass(eq=False)
class GroupNotFoundException(LogicException):
    oid: str

    @property
    def message(self):
        return f"Group with {self.oid=} was not found"


@dataclass(eq=False)
class InvalidCredentialsException(LogicException):
    @property
    def message(self):
        return "Invalid credentials were provided"

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
    password: str

    @property
    def message(self) -> str:
        return f"Password length is not valid: {len(self.password)}"


@dataclass(eq=False)
class EmptyEmail(ApplicationException):
    @property
    def message(self) -> str:
        return "Email is empty"


class EmptyGroupTitle(ApplicationException):
    @property
    def message(self) -> str:
        return "Group title is empty"


@dataclass(eq=False)
class GroupTitleLengthIsNotValid(ApplicationException):
    title: str

    @property
    def message(self) -> str:
        return f"Group title length is not valid: {self.title}"

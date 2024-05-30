from dataclasses import dataclass

from domain.exceptions.base import ApplicationException
from http import HTTPStatus


@dataclass(eq=False)
class InvalidUsernameLength(ApplicationException):
    username_value: str

    @property
    def message(self) -> str:
        return f"Username length is invalid: {self.username_value}"

    @property
    def status_code(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class EmptyUsername(ApplicationException):
    @property
    def message(self) -> str:
        return "Username is empty"

    @property
    def status_code(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class EmptyPassword(ApplicationException):
    @property
    def message(self) -> str:
        return "Password is empty"

    @property
    def status_code(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class InvalidPasswordLength(ApplicationException):
    length: str

    @property
    def message(self) -> str:
        return f"Password length is invalid: {self.length}"

    @property
    def status_code(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class EmptyEmail(ApplicationException):
    @property
    def message(self) -> str:
        return "Email is empty"

    @property
    def status_code(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class InvalidEmail(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f"The provided email is invalid: {self.email}"

    @property
    def status_code(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value

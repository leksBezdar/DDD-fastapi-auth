from dataclasses import dataclass

from http import HTTPStatus

from infrastructure.exceptions.base import InfrastructureException


@dataclass(eq=False)
class InvalidToken(InfrastructureException):
    @property
    def message(self) -> str:
        return "Token is invalid"

    @property
    def status_code(self) -> int:
        return HTTPStatus.UNAUTHORIZED.value


@dataclass(eq=False)
class ExpiredToken(InfrastructureException):
    @property
    def message(self) -> str:
        return "Token has expired"

    @property
    def status_code(self) -> int:
        return HTTPStatus.UNAUTHORIZED.value

from dataclasses import dataclass

from domain.exceptions.base import ApplicationException
from http import HTTPStatus


class EmptyGroupTitle(ApplicationException):
    @property
    def message(self) -> str:
        return "Group title is empty"

    @property
    def status_code(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


@dataclass(eq=False)
class InvalidGroupTitleLength(ApplicationException):
    title: str

    @property
    def message(self) -> str:
        return f"Group title length is not valid: {self.title}"

    @property
    def status_code(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value

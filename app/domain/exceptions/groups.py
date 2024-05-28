from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


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

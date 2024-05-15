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
    @property
    def message(self):
        return "Username is empty"


class EmptyGroupTitle(ApplicationException):
    @property
    def message(self):
        return "Group title is empty"


@dataclass(eq=False)
class GroupTitleTooLong(ApplicationException):
    title: str

    @property
    def message(self):
        return f"Group title is too long: {self.title}"

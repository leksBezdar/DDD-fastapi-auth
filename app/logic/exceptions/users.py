from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class GroupAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f"Group with that title already exists: {self.title}"

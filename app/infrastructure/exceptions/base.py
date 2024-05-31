from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class InfrastructureException(ApplicationException):
    @property
    def message(self) -> str:
        return "Infrastructure exeption has occurred"

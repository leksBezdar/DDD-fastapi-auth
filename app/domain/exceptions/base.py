from dataclasses import dataclass
from http import HTTPStatus


@dataclass(eq=False)
class ApplicationException(Exception):
    @property
    def message(self) -> str:
        return "An application error has occurred"

    @property
    def status_code(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value

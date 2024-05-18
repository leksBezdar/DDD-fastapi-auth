from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar


@dataclass(frozen=True)
class BaseCommand(ABC): ...


CT = TypeVar(name="CT", bound="BaseCommand")
CR = TypeVar(name="CR", bound=any)


@dataclass(frozen=True)
class CommandHandler(ABC, Generic[CT, CR]):
    @abstractmethod
    async def handle(self, commant: CT) -> CR: ...
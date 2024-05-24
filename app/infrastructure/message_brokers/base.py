from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def send_message(self, key: str, topic: str, value: bytes): ...

    @abstractmethod
    async def consume(self, topic: str): ...

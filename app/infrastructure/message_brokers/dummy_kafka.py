from dataclasses import dataclass, field

from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class DummyKafkaMessageBroker(BaseMessageBroker):
    _messages: dict[str, list[bytes]] = field(default_factory=lambda: {})

    async def start(self) -> None:
        print("Dummy Kafka broker started")

    async def stop(self) -> None:
        print("Dummy Kafka broker stopped")

    async def send_message(self, key: str, topic: str, value: bytes) -> None:
        if topic not in self._messages:
            self._messages[topic] = []
        self._messages[topic].append(value)
        print(f"Dummy sent message to topic {topic}: {value}")

    async def start_consuming(self, topic: str) -> list[bytes]:
        return self._messages.get(topic, [])

    async def stop_consuming(self, topic: str):
        print(f"Dummy stopped consuming messages from topic {topic}")

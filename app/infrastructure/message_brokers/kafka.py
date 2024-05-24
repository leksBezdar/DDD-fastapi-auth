from dataclasses import dataclass

from infrastructure.message_brokers.base import BaseMessageBroker
from aiokafka import AIOKafkaProducer


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer

    async def send_message(self, key: bytes, topic: str, value: bytes):
        await self.producer.send(key=key, topic=topic, value=value)

    async def consume(self, topic: str): ...

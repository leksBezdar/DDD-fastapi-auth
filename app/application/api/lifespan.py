from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.message_brokers.kafka import KafkaMessageBroker
from logic.init import init_container


async def start_kafka():
    container = init_container()
    message_broker: KafkaMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.producer.start()


async def close_kafka():
    container = init_container()
    message_broker: KafkaMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.producer.stop()

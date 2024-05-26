from dataclasses import dataclass

from domain.events.users import (
    GroupDeletedEvent,
    NewGroupCreatedEvent,
    NewUserCreatedEvent,
)
from infrastructure.message_brokers.converters import convert_event_to_broker_message
from logic.events.base import EventHandler


@dataclass
class NewGroupCreatedEventHandler(EventHandler[NewGroupCreatedEvent, None]):
    async def handle(self, event: NewGroupCreatedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=event.event_id.encode(),
        )


@dataclass
class NewUserCreatedEventHandler(EventHandler[NewUserCreatedEvent, None]):
    async def handle(self, event: NewUserCreatedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=event.event_id.encode(),
        )


@dataclass
class GroupDeletedEventHandler(EventHandler[GroupDeletedEvent, None]):
    async def handle(self, event: GroupDeletedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=event.event_id.encode(),
        )

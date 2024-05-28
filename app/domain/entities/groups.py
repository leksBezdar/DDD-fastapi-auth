from dataclasses import field, dataclass

from domain.entities.base import BaseEntity
from domain.values.groups import Title
from domain.events.groups import (
    GroupDeletedEvent,
    GroupCreatedEvent,
)


@dataclass(eq=False)
class UserGroup(BaseEntity):
    title: Title
    is_deleted: bool = field(default=False, kw_only=True)

    @classmethod
    def create(cls, title: Title) -> "UserGroup":
        new_group = cls(title=title)
        new_group.register_event(
            GroupCreatedEvent(
                group_title=new_group.title.as_generic_type(),
                group_oid=new_group.oid,
            )
        )

        return new_group

    def delete(self) -> None:
        self.is_deleted = True
        self.register_event(
            GroupDeletedEvent(
                group_oid=self.oid, group_title=self.title.as_generic_type()
            )
        )

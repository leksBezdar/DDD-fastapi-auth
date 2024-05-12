from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.base import BaseEntity
from domain.values.users import Username


@dataclass(eq=False)
class User(BaseEntity):
    username: Username
    created_at: datetime = field(
        default_factory=datetime.now(),
        kw_only=True,
    )

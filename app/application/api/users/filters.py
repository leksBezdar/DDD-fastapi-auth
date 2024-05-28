from dataclasses import dataclass

from infrastructure.repositories.users.filters.users import (
    GetUsersFilters as GetUsersInfrastructureFilters,
)


@dataclass
class GetUsersFilters:
    limit: int = 10
    offset: int = 0

    def to_infrastructure_filters(self):
        return GetUsersInfrastructureFilters(limit=self.limit, offset=self.offset)

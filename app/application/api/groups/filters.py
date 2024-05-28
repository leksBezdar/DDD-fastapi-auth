from dataclasses import dataclass

from infrastructure.repositories.groups.filters.groups import (
    GetGroupsFilters as GetGroupsInfrastructureFilters,
)


@dataclass
class GetGroupsFilters:
    limit: int = 10
    offset: int = 0

    def to_infrastructure_filters(self):
        return GetGroupsInfrastructureFilters(limit=self.limit, offset=self.offset)

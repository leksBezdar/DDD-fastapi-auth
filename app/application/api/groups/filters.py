from dataclasses import dataclass

from application.api.common.filters.base import BaseGetAllFilters
from infrastructure.repositories.groups.filters.groups import (
    GetGroupsFilters as GetGroupsInfrastructureFilters,
)


@dataclass
class GetGroupsFilters(BaseGetAllFilters):
    limit: int = 10
    offset: int = 0

    def to_infrastructure_filters(self):
        return GetGroupsInfrastructureFilters(limit=self.limit, offset=self.offset)

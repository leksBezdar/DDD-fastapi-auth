from dataclasses import dataclass

from infrastructure.repositories.common.filters.base import BaseGetAllFilters


@dataclass
class GetGroupsFilters(BaseGetAllFilters):
    limit: int = 10
    offset: int = 0

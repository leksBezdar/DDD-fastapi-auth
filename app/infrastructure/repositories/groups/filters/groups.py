from dataclasses import dataclass


@dataclass
class GetGroupsFilters:
    limit: int = 10
    offset: int = 0

from dataclasses import dataclass


@dataclass
class GetUsersFilters:
    limit: int = 10
    offset: int = 0


@dataclass
class GetGroupsFilters:
    limit: int = 10
    offset: int = 0

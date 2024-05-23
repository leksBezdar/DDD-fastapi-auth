from dataclasses import dataclass


@dataclass
class GetUsersFilters:
    limit: int = 10
    offset: int = 0

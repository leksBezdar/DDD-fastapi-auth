from datetime import datetime
import pytest
from faker import Faker

from domain.entities.groups import UserGroup
from domain.exceptions.groups import (
    EmptyGroupTitle,
    GroupTitleLengthIsNotValid,
)
from domain.values.groups import Title


def test_create_user_group_success(faker: Faker) -> None:
    title = Title(faker.text(15))
    group = UserGroup(title=title)

    assert group.title == title
    assert not group.is_deleted
    assert group.created_at.date() == datetime.today().date()


def test_create_user_group_empty_title() -> None:
    with pytest.raises(EmptyGroupTitle):
        Title("")


def test_create_user_group_short_title(faker: Faker) -> None:
    with pytest.raises(GroupTitleLengthIsNotValid):
        Title(faker.word(ext_word_list=["ac", "ba"]))


def test_create_user_group_long_title(faker: Faker) -> None:
    with pytest.raises(GroupTitleLengthIsNotValid):
        Title(faker.text(15) * 50)

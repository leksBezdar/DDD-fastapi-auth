from datetime import datetime
from uuid import uuid4
from faker import Faker
import pytest

from domain.entities.users import User, UserGroup
from domain.events.users import NewUserCreatedEvent
from domain.exceptions.users import (
    EmptyGroupTitle,
    EmptyPassword,
    EmptyUsername,
    GroupTitleLengthIsNotValid,
    InvalidEmail,
    PasswordLengthIsNotValid,
    UsernameLengthIsNotValid,
)
from domain.values.users import Email, Password, Username, Title


def test_create_user_success(faker: Faker) -> None:
    username = Username(faker.text(15))
    email = Email(faker.email(15))
    password = Password(faker.text(15))
    user = User(
        email=email,
        username=username,
        password=password,
        group_id=str(uuid4()),
    )

    assert user.email == email
    assert user.username == username
    assert user.password == password
    assert user.created_at.date() == datetime.today().date()


def test_create_user_empty_username() -> None:
    with pytest.raises(EmptyUsername):
        Username("")


def test_create_user_short_username() -> None:
    with pytest.raises(UsernameLengthIsNotValid):
        Username("u")


def test_create_user_long_username() -> None:
    with pytest.raises(UsernameLengthIsNotValid):
        Username("Leks" * 100)


def test_create_user_empty_password() -> None:
    with pytest.raises(EmptyPassword):
        Password("")


def test_create_user_short_password() -> None:
    with pytest.raises(PasswordLengthIsNotValid):
        Password("p")


def test_create_user_long_password() -> None:
    with pytest.raises(PasswordLengthIsNotValid):
        Password("password" * 100)


def test_create_user_invalid_email() -> None:
    with pytest.raises(InvalidEmail):
        Email("invalid_email")


def test_create_user_group_success() -> None:
    title = Title("title")
    group = UserGroup(title=title)

    assert group.title == title
    assert not group.users
    assert group.created_at.date() == datetime.today().date()


def test_create_user_group_empty_title() -> None:
    with pytest.raises(EmptyGroupTitle):
        Title("")


def test_create_user_group_short_title() -> None:
    with pytest.raises(GroupTitleLengthIsNotValid):
        Title("t")


def test_create_user_group_long_title() -> None:
    with pytest.raises(GroupTitleLengthIsNotValid):
        Title("wrong_title" * 50)


def test_add_user_to_user_group(faker: Faker) -> None:
    username = Username(faker.text(15))
    email = Email(faker.email(15))
    password = Password(faker.text(15))
    user = User(
        email=email,
        username=username,
        password=password,
        group_id=str(uuid4()),
    )

    title = Title(faker.text(15))
    group = UserGroup(title=title)

    group.add_user(user)

    assert user in group.users


def test_new_user_events(faker: Faker) -> None:
    username = Username(faker.text(15))
    email = Email(faker.email(15))
    password = Password(faker.text(15))
    user = User(
        email=email,
        username=username,
        password=password,
        group_id=str(uuid4()),
    )

    title = Title(faker.text(15))
    group = UserGroup(title=title)

    group.add_user(user)
    events = group.pull_events()
    pulled_events = group.pull_events()

    assert not pulled_events, pulled_events
    assert len(events) == 1, events

    new_event = events[0]

    assert isinstance(new_event, NewUserCreatedEvent), new_event
    assert new_event.group_oid == group.oid
    assert new_event.username == user.username.as_generic_type()
    assert new_event.user_oid == user.oid

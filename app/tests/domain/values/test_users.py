from datetime import datetime
from uuid import uuid4
from faker import Faker
import pytest

from domain.entities.users import User
from domain.exceptions.users import (
    EmptyPassword,
    EmptyUsername,
    InvalidEmail,
    InvalidPasswordLength,
    InvalidUsernameLength,
)
from domain.values.users import Email, Password, Username


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
    assert not user.is_verified


def test_create_user_empty_username() -> None:
    with pytest.raises(EmptyUsername):
        Username("")


def test_create_user_short_username(faker: Faker) -> None:
    with pytest.raises(InvalidUsernameLength):
        Username(faker.word(ext_word_list=["ac", "ba"]))


def test_create_user_long_username(faker: Faker) -> None:
    with pytest.raises(InvalidUsernameLength):
        Username(faker.text(15) * 15)


def test_create_user_empty_password() -> None:
    with pytest.raises(EmptyPassword):
        Password("")


def test_create_user_short_password(faker: Faker) -> None:
    with pytest.raises(InvalidPasswordLength):
        Password(faker.word(ext_word_list=["ac", "ba"]))


def test_create_user_long_password(faker: Faker) -> None:
    with pytest.raises(InvalidPasswordLength):
        Password(faker.text(15) * 15)


def test_create_user_invalid_email() -> None:
    with pytest.raises(InvalidEmail):
        Email("invalid_email")

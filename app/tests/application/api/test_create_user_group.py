from faker import Faker

from httpx import Response
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
import pytest


@pytest.mark.asyncio
async def test_create_group_success(app: FastAPI, client: TestClient, faker: Faker):
    url = app.url_path_for("create_group")
    title = faker.text(15)
    response: Response = client.post(url=url, json={"title": title})
    assert response.is_success
    json_data = response.json()

    assert json_data["title"] == title


@pytest.mark.asyncio
async def test_create_group_title_too_long(
    app: FastAPI, client: TestClient, faker: Faker
):
    url = app.url_path_for("create_group")
    title = faker.text(150)
    response: Response = client.post(url=url, json={"title": title})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()
    json_data = response.json()

    assert json_data["detail"]


@pytest.mark.asyncio
async def test_create_group_title_empty(
    app: FastAPI,
    client: TestClient,
):
    url = app.url_path_for("create_group")
    response: Response = client.post(url=url, json={"title": ""})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()
    json_data = response.json()

    assert json_data["detail"]

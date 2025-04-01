import pytest


@pytest.mark.asyncio
async def test_login_user_not_found(client):
    data = {
        "username": "test1",
        "password": "test1"
    }

    response = await client.post("/users", json=data)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    data = {
        "username": "test",
        "password": "test1"
    }

    response = await client.post("/users", json=data)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_success(client):
    data = {
        "username": "test",
        "password": "test"
    }

    response = await client.post("/users", json=data)

    assert response.status_code == 200

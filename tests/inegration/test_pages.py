import pytest


@pytest.mark.asyncio
async def test_add_page(client):
    data = {
        "url": "test-test-page",
        "content": [
            {"blockId": ":r1:", "content": "123123123", "type": "text"},
            {"blockId": ":r2:", "content": "123123123", "type": "image"},
            {"blockId": ":r3:", "content": "123123123", "type": "video"},
        ],
    }

    response = await client.post("/pages", json=data)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_page_urls(client):
    response = await client.get("/pages")

    assert response.status_code == 200

    resp_data = response.json()

    assert len(resp_data) == 1
    assert resp_data[0] == "test-test-page"


@pytest.mark.asyncio
async def test_get_page_full_data(client):
    response = await client.get("/pages/test-test-page")

    assert response.status_code == 200

    resp_data = response.json()

    assert resp_data["url"] == "test-test-page"
    assert len(resp_data["content"]) == 3
    assert resp_data["content"][0]["blockId"] == ":r1:"
    assert resp_data["content"][1]["blockId"] == ":r2:"
    assert resp_data["content"][2]["blockId"] == ":r3:"


@pytest.mark.asyncio
async def test_delete_page(client):
    response = await client.delete("/pages/test-test-page")

    assert response.status_code == 200

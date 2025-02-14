import pytest


@pytest.mark.asyncio
async def test_add_headers(client):
    data = [
        {
            "headerName": "Студенту",
            "headerUrl": None,
            "tabs": [
                {"tabName": "Вступ", "tabUrl": "https://youtube.com"},
                {"tabName": "Стипендія", "tabUrl": None},
            ],
        },
        {"headerName": "Викладачу", "headerUrl": "https://youtube.com", "tabs": []},
    ]

    response = await client.post("/headers", json=data)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_headers(client):
    response = await client.get("/headers")

    assert response.status_code == 200

    resp_data = response.json()

    assert len(resp_data) == 2
    assert resp_data[0]["headerName"] == "Студенту"
    assert resp_data[0]["tabs"][0]["tabName"] == "Вступ"

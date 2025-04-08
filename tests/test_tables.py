from datetime import datetime, timedelta

import pytest


@pytest.mark.asyncio
async def test_create_table(async_client):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    table_data = {
        "name": f"Test Table Create {timestamp}",
        "seats": 4,
        "location": "Сад",
    }

    create_response = await async_client.post("/tables/", json=table_data)

    assert create_response.status_code == 201
    assert create_response.json()["detail"] == "Table created successfully"

    table_id = create_response.json()["id"]
    assert table_id is not None


@pytest.mark.asyncio
async def test_delete_table(async_client):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    table_data = {
        "name": f"Test Table Delete {timestamp}",
        "seats": 2,
        "location": "Терраса",
    }

    create_response = await async_client.post("/tables/", json=table_data)
    table_id = create_response.json()["id"]

    assert create_response.status_code == 201

    delete_response = await async_client.delete(f"/tables/{table_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["transaction"] == "Table delete is successful"


@pytest.mark.asyncio
async def test_get_all_tables(async_client):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    table_data = [
        {"name": f"Test Table Get {timestamp} A", "seats": 4, "location": "Сад"},
        {"name": f"Test Table Get {timestamp} B", "seats": 2, "location": "Терраса"},
    ]

    for table in table_data:
        await async_client.post("/tables/", json=table)

    response = await async_client.get("/tables/")

    assert response.status_code == 200

    tables = response.json()
    assert isinstance(tables, list)
    assert len(tables) > 0

    for table in table_data:
        assert any(table["name"] in t["name"] for t in tables)

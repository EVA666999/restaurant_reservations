import asyncio
from datetime import datetime, timedelta

import pytest


@pytest.mark.asyncio
async def test_create_reservation(async_client):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    table_data = {"name": f"Test Table Get {timestamp}", "seats": 4, "location": "Сад"}
    table_response = await async_client.post("/tables/", json=table_data)
    table_id = table_response.json()["id"]

    await asyncio.sleep(1)

    reservation_data = {
        "customer_name": "Jane Doe",
        "table_id": table_id,
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": 90,
    }
    create_response = await async_client.post("/reservations/", json=reservation_data)

    assert create_response.status_code == 201
    assert create_response.json()["detail"] == "Reservation created successfully"
    reservation_id = create_response.json()["id"]

    assert reservation_id is not None


@pytest.mark.asyncio
async def test_get_all_reservations(async_client):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    table_data = {"name": f"Test Table Get {timestamp}", "seats": 4, "location": "Сад"}
    table_response = await async_client.post("/tables/", json=table_data)
    table_id = table_response.json()["id"]

    await asyncio.sleep(1)

    reservation_data = {
        "customer_name": "Jane Doe",
        "table_id": table_id,
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": 90,
    }
    create_response = await async_client.post("/reservations/", json=reservation_data)

    assert create_response.status_code == 201
    assert create_response.json()["detail"] == "Reservation created successfully"

    get_response = await async_client.get("/reservations/")

    assert get_response.status_code == 200
    reservations = get_response.json()
    assert isinstance(reservations, list)
    assert len(reservations) > 0


@pytest.mark.asyncio
async def test_delete_reservation(async_client):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    table_data = {
        "name": f"Test Table Delete {timestamp}",
        "seats": 2,
        "location": "Терраса",
    }
    table_response = await async_client.post("/tables/", json=table_data)
    table_id = table_response.json()["id"]

    await asyncio.sleep(1)

    reservation_data = {
        "customer_name": "John Smith",
        "table_id": table_id,
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": 30,
    }
    create_response = await async_client.post("/reservations/", json=reservation_data)
    reservation_id = create_response.json()["id"]

    await asyncio.sleep(1)

    response = await async_client.delete(f"/reservations/{reservation_id}")
    assert response.status_code == 200
    assert response.json()["transaction"] == "Reservation delete is successful"

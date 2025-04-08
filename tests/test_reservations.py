import asyncio
import pytest
from datetime import datetime, timedelta
import asyncio
import pytest
from datetime import datetime, timedelta

import asyncio
import pytest
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_reservation(async_client):
    table_data = {"name": "Test Table Create", "seats": 4, "location": "Главный зал"}
    table_response = await async_client.post("/tables/", json=table_data)
    table_id = table_response.json()["id"]

    await asyncio.sleep(1)  # Добавьте задержку после создания стола

    reservation_data = {
        "customer_name": "John Doe",
        "table_id": table_id,
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": 60
    }
    
    response = await async_client.post("/reservations/", json=reservation_data)
    assert response.status_code == 201
    result = response.json()
    assert "id" in result
    assert result["detail"] == "Reservation created successfully"

@pytest.mark.asyncio
async def test_delete_reservation(async_client):
    table_data = {"name": "Test Table Delete", "seats": 2, "location": "Терраса"} 
    table_response = await async_client.post("/tables/", json=table_data)
    table_id = table_response.json()["id"]

    await asyncio.sleep(1)  # Добавьте задержку после создания стола

    reservation_data = {
        "customer_name": "John Smith",
        "table_id": table_id, 
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": 30
    }
    create_response = await async_client.post("/reservations/", json=reservation_data)
    reservation_id = create_response.json()["id"]

    await asyncio.sleep(1)  # Добавьте задержку после создания брони

    response = await async_client.delete(f"/reservations/{reservation_id}")
    assert response.status_code == 200
    assert response.json()["transaction"] == "Reservation delete is successful"

@pytest.mark.asyncio
async def test_create_reservation(async_client):
    table_data = {"name": "Test Table Create", "seats": 4, "location": "Главный зал"}
    table_response = await async_client.post("/tables/", json=table_data)
    table_id = table_response.json()["id"]

    await asyncio.sleep(1)  # Добавьте задержку после создания стола

    reservation_data = {
        "customer_name": "John Doe",
        "table_id": table_id,
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": 60
    }
    
    response = await async_client.post("/reservations/", json=reservation_data)
    assert response.status_code == 201
    result = response.json()
    assert "id" in result
    assert result["detail"] == "Reservation created successfully"

@pytest.mark.asyncio
async def test_delete_reservation(async_client):
    table_data = {"name": "Test Table Delete", "seats": 2, "location": "Терраса"} 
    table_response = await async_client.post("/tables/", json=table_data)
    table_id = table_response.json()["id"]

    await asyncio.sleep(1)  # Добавьте задержку после создания стола

    reservation_data = {
        "customer_name": "John Smith",
        "table_id": table_id, 
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": 30
    }
    create_response = await async_client.post("/reservations/", json=reservation_data)
    reservation_id = create_response.json()["id"]

    await asyncio.sleep(1)  # Добавьте задержку после создания брони

    response = await async_client.delete(f"/reservations/{reservation_id}")
    assert response.status_code == 200
    assert response.json()["transaction"] == "Reservation delete is successful"
import pytest


def test_get_tables(client):
    """Тест GET /tables/ - получение списка столов"""
    response = client.get("/tables/")
    assert response.status_code in [200, 404]
    
    if response.status_code == 200:
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_table(async_client):
    """Тест POST /tables/ - создание нового стола"""
    data = {
        "name": "Тестовый стол",
        "seats": 4,
        "location": "Терраса"  # Используем правильное значение из перечисления
    }
    
    # Используем асинхронный клиент для предотвращения проблем с циклом событий
    response = await async_client.post("/tables/", json=data)
    assert response.status_code == 201
    
    # Проверяем ответ
    result = response.json()
    assert "id" in result
    assert result["detail"] == "Table created successfully"
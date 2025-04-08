import sys
import os
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest_asyncio

# Добавляем корневую директорию проекта в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


@pytest.fixture
def client():
    """Синхронный тестовый клиент для API"""
    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture
async def async_client():
    """Асинхронный тестовый клиент для API"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
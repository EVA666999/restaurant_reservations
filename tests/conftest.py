import asyncio
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
import sys
import os
import pytest_asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()
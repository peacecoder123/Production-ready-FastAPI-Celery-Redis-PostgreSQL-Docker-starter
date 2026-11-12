import asyncio
import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import create_tables, drop_tables
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    asyncio.run(create_tables())
    yield
    asyncio.run(drop_tables())


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

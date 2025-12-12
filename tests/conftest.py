import sys
from datetime import timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add parent directory to path so we can import main
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app  # noqa: E402
from auth.security import create_access_token  # noqa: E402


@pytest.fixture
def client():
    """Fixture untuk TestClient"""
    return TestClient(app)


@pytest.fixture
def token():
    """Fixture untuk generate JWT token valid"""
    access_token = create_access_token(
        data={"sub": "azizdzaki"},
        expires_delta=timedelta(minutes=30)
    )
    return access_token


@pytest.fixture
def auth_headers(token):
    """Fixture untuk authorization headers"""
    return {"Authorization": f"Bearer {token}"}

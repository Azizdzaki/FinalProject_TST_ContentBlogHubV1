import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from datetime import timedelta

# Add parent directory to path so we can import main
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from auth.security import create_access_token

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

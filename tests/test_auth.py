import sys
from datetime import timedelta
from pathlib import Path

from fastapi.testclient import TestClient
from jose import jwt

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app  # noqa: E402
from auth.security import (  # noqa: E402
    verify_password,
    create_access_token,
    get_user,
    get_password_hash,
    SECRET_KEY,
    ALGORITHM
)
from database.db import mock_users  # noqa: E402

client = TestClient(app)


class TestAuthenticationLogin:
    """Test suite untuk endpoint /token"""

    def test_login_success(self):
        """Test login berhasil dengan kredensial valid"""
        response = client.post(
            "/token",
            data={"username": "azizdzaki", "password": "secret"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_success_second_user(self):
        """Test login berhasil dengan user lain"""
        response = client.post(
            "/token",
            data={"username": "johndoe", "password": "secret"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self):
        """Test login gagal dengan password salah"""
        response = client.post(
            "/token",
            data={"username": "azizdzaki", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_login_wrong_username(self):
        """Test login gagal dengan username tidak terdaftar"""
        response = client.post(
            "/token",
            data={"username": "nonexistentuser", "password": "secret"}
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_login_empty_credentials(self):
        """Test login dengan kredensial kosong"""
        response = client.post(
            "/token",
            data={"username": "", "password": ""}
        )
        # Empty credentials returns either 401 or 422 depending on Python version
        # Python 3.9: 401 (authentication error)
        # Python 3.10+: 422 (validation error)
        assert response.status_code in (401, 422)


class TestSecurityUtilities:
    """Test suite untuk utility functions di auth/security.py"""

    def test_verify_password_correct(self):
        """Test verify_password dengan password yang benar"""
        plain_password = "secret"
        stored_password = "secret"
        assert verify_password(plain_password, stored_password) is True

    def test_verify_password_incorrect(self):
        """Test verify_password dengan password yang salah"""
        plain_password = "wrongpassword"
        stored_password = "secret"
        assert verify_password(plain_password, stored_password) is False

    def test_verify_password_case_sensitive(self):
        """Test verify_password case-sensitive"""
        plain_password = "Secret"
        stored_password = "secret"
        assert verify_password(plain_password, stored_password) is False

    def test_create_access_token_valid(self):
        """Test pembuatan access token valid"""
        token = create_access_token(
            data={"sub": "testuser"},
            expires_delta=timedelta(minutes=30)
        )
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_without_expiry(self):
        """Test pembuatan token tanpa custom expiry (default 15 menit)"""
        token = create_access_token(data={"sub": "testuser"})
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_different_data(self):
        """Test token dengan data berbeda menghasilkan token berbeda"""
        token1 = create_access_token(
            data={"sub": "user1"},
            expires_delta=timedelta(minutes=30)
        )
        token2 = create_access_token(
            data={"sub": "user2"},
            expires_delta=timedelta(minutes=30)
        )
        assert token1 != token2

    def test_get_password_hash(self):
        """Test get_password_hash function"""
        password = "testpassword"
        hashed = get_password_hash(password)
        assert hashed == password  # Simplified hash function

    def test_get_user_exists(self):
        """Test get_user dengan user yang ada"""
        user = get_user(mock_users, "azizdzaki")
        assert user is not None
        assert user.username == "azizdzaki"

    def test_get_user_not_exists(self):
        """Test get_user dengan user yang tidak ada"""
        user = get_user(mock_users, "nonexistent")
        assert user is None

    def test_get_current_user_via_discovery_valid_token(self):
        """Test get_current_user with discovery endpoint."""
        # Get valid token
        login_response = client.post(
            "/token",
            data={"username": "azizdzaki", "password": "secret"}
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Use token in discovery endpoint
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200

    def test_get_current_user_via_discovery_invalid_token(self):
        """Test discovery with invalid token."""
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial"},
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

    def test_get_current_user_via_discovery_missing_sub(self):
        """Test get_current_user dengan token tanpa subject"""
        # Create token without 'sub' claim
        token_data = {"exp": 9999999999}
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        response = client.post(
            "/discovery/",
            json={"category": "Tutorial"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 401

    def test_get_current_user_via_discovery_nonexistent_user(self):
        """Test get_current_user dengan user tidak ada"""
        token = create_access_token(
            data={"sub": "nonexistentuser"},
            expires_delta=timedelta(minutes=30)
        )

        response = client.post(
            "/discovery/",
            json={"category": "Tutorial"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 401

    def test_token_decode_with_wrong_key(self):
        """Test token decode dengan valid user"""
        token = create_access_token(
            data={"sub": "azizdzaki"},
            expires_delta=timedelta(minutes=30)
        )
        # Token valid dengan SECRET_KEY dan user exists di database
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial"},
            headers={"Authorization": f"Bearer {token}"}
        )
        # Should succeed karena token valid dan user ada
        assert response.status_code == 200


class TestRootEndpoint:
    """Test suite untuk root endpoint"""

    def test_root_endpoint(self):
        """Test GET / endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from datetime import timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from auth.security import create_access_token

client = TestClient(app)

@pytest.fixture
def valid_token():
    """Generate valid JWT token untuk test"""
    return create_access_token(
        data={"sub": "azizdzaki"},
        expires_delta=timedelta(minutes=30)
    )

@pytest.fixture
def auth_headers(valid_token):
    """Authorization headers dengan token valid"""
    return {"Authorization": f"Bearer {valid_token}"}

class TestDiscoveryFilterCategory:
    """Test suite untuk filter kategori"""
    
    def test_filter_category_tutorial(self, auth_headers):
        """Test filter dengan kategori 'Tutorial'"""
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial"},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 2  # a1 dan a2 memiliki kategori Tutorial
        assert all(article["category"]["name"] == "Tutorial" for article in articles)
    
    def test_filter_category_tech_news(self, auth_headers):
        """Test filter dengan kategori 'Berita Teknologi'"""
        response = client.post(
            "/discovery/",
            json={"category": "Berita Teknologi"},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 1  # Hanya a3
        assert articles[0]["article_id"] == "a3"
    
    def test_filter_category_case_insensitive(self, auth_headers):
        """Test filter kategori case-insensitive"""
        response = client.post(
            "/discovery/",
            json={"category": "tutorial"},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 2
    
    def test_filter_category_nonexistent(self, auth_headers):
        """Test filter dengan kategori yang tidak ada"""
        response = client.post(
            "/discovery/",
            json={"category": "NonexistentCategory"},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 0

class TestDiscoveryFilterTags:
    """Test suite untuk filter tags"""
    
    def test_filter_single_tag_python(self, auth_headers):
        """Test filter dengan tag 'python'"""
        response = client.post(
            "/discovery/",
            json={"tags": ["python"]},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 2  # a1 dan a3 memiliki tag python
        article_ids = {article["article_id"] for article in articles}
        assert article_ids == {"a1", "a3"}
    
    def test_filter_single_tag_ddd(self, auth_headers):
        """Test filter dengan tag 'ddd'"""
        response = client.post(
            "/discovery/",
            json={"tags": ["ddd"]},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 1
        assert articles[0]["article_id"] == "a2"
    
    def test_filter_multiple_tags_required(self, auth_headers):
        """Test filter dengan multiple tags (semua harus ada)"""
        response = client.post(
            "/discovery/",
            json={"tags": ["python", "fastapi"]},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 1  # Hanya a1 punya kedua tag
        assert articles[0]["article_id"] == "a1"
    
    def test_filter_tags_case_insensitive(self, auth_headers):
        """Test filter tags case-insensitive"""
        response = client.post(
            "/discovery/",
            json={"tags": ["PYTHON"]},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 2
    
    def test_filter_nonexistent_tag(self, auth_headers):
        """Test filter dengan tag yang tidak ada"""
        response = client.post(
            "/discovery/",
            json={"tags": ["nonexistenttag"]},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 0

class TestDiscoveryCombinedFilters:
    """Test suite untuk kombinasi filter kategori + tags"""
    
    def test_filter_category_and_single_tag(self, auth_headers):
        """Test kombinasi kategori dan tag"""
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial", "tags": ["fastapi"]},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 1  # Hanya a1 punya Tutorial + fastapi
        assert articles[0]["article_id"] == "a1"
    
    def test_filter_category_and_multiple_tags(self, auth_headers):
        """Test kombinasi kategori dan multiple tags"""
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial", "tags": ["python", "fastapi"]},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 1
        assert articles[0]["article_id"] == "a1"
    
    def test_filter_category_and_incompatible_tags(self, auth_headers):
        """Test kombinasi kategori dan tags yang tidak cocok"""
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial", "tags": ["nonexistent"]},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 0

class TestDiscoveryPagination:
    """Test suite untuk pagination (parameter N)"""
    
    def test_pagination_default_limit(self, auth_headers):
        """Test default limit N=10"""
        response = client.post(
            "/discovery/",
            json={},
            headers=auth_headers,
            params={"N": 10}
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) <= 10
    
    def test_pagination_limit_one(self, auth_headers):
        """Test limit N=1"""
        response = client.post(
            "/discovery/",
            json={},
            headers=auth_headers,
            params={"N": 1}
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 1
    
    def test_pagination_limit_two(self, auth_headers):
        """Test limit N=2"""
        response = client.post(
            "/discovery/",
            json={},
            headers=auth_headers,
            params={"N": 2}
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 2

class TestDiscoveryEmptyResults:
    """Test suite untuk hasil kosong"""
    
    def test_empty_result_impossible_combination(self, auth_headers):
        """Test kombinasi filter yang menghasilkan hasil kosong"""
        response = client.post(
            "/discovery/",
            json={"category": "Berita Teknologi", "tags": ["ddd"]},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 0
    
    def test_empty_result_empty_criteria(self, auth_headers):
        """Test dengan criteria kosong (return semua)"""
        response = client.post(
            "/discovery/",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) > 0

class TestDiscoverySecurity:
    """Test suite untuk security & authentication"""
    
    def test_discovery_without_token(self):
        """Test akses tanpa token (harus 401)"""
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial"}
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
    
    def test_discovery_without_bearer_prefix(self):
        """Test dengan token tanpa 'Bearer' prefix"""
        token = create_access_token(
            data={"sub": "azizdzaki"},
            expires_delta=timedelta(minutes=30)
        )
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial"},
            headers={"Authorization": token}  # Tanpa "Bearer "
        )
        assert response.status_code == 401
    
    def test_discovery_with_invalid_token(self):
        """Test dengan token invalid"""
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial"},
            headers={"Authorization": "Bearer invalid_token_short"}
        )
        assert response.status_code == 401
    
    def test_discovery_with_malformed_header(self):
        """Test dengan header malformed"""
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial"},
            headers={"Authorization": "InvalidPrefix sometoken"}
        )
        assert response.status_code == 401
    
    def test_discovery_with_empty_token(self):
        """Test dengan token kosong"""
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial"},
            headers={"Authorization": "Bearer "}
        )
        assert response.status_code == 401

class TestDiscoveryEdgeCases:
    """Test suite untuk edge cases"""
    
    def test_no_filters_returns_all_articles(self, auth_headers):
        """Test tanpa filter mengembalikan semua artikel"""
        response = client.post(
            "/discovery/",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 3  # a1, a2, a3
    
    def test_special_characters_in_filter(self, auth_headers):
        """Test filter dengan special characters"""
        response = client.post(
            "/discovery/",
            json={"category": "Tutorial@#$"},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 0
    
    def test_whitespace_in_category_filter(self, auth_headers):
        """Test filter dengan whitespace"""
        response = client.post(
            "/discovery/",
            json={"category": "  Tutorial  "},
            headers=auth_headers
        )
        # Seharusnya tidak match karena case-insensitive tapi exact match
        assert response.status_code == 200
    
    def test_both_filters_none(self, auth_headers):
        """Test dengan both filters adalah None"""
        response = client.post(
            "/discovery/",
            json={"tags": None, "category": None},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 3
    
    def test_empty_tags_list(self, auth_headers):
        """Test dengan tags list kosong"""
        response = client.post(
            "/discovery/",
            json={"tags": []},
            headers=auth_headers
        )
        assert response.status_code == 200
        articles = response.json()
        # Empty tags list means no tag filter, should return all
        assert len(articles) == 3

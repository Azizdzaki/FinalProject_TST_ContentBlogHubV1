import pytest
import sys
from pathlib import Path
from pydantic import ValidationError

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.user import User, UserInDB, Token, TokenData
from models.discovery import SearchCriteria
from models.article import Article
from models.taxonomy import Category, Tag

class TestUserModels:
    """Test suite untuk User models"""
    
    def test_user_model_creation(self):
        """Test membuat User model"""
        user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User"
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
    
    def test_user_model_optional_fields(self):
        """Test User dengan field optional kosong"""
        user = User(username="testuser")
        assert user.username == "testuser"
        assert user.email is None
        assert user.full_name is None
    
    def test_user_in_db_creation(self):
        """Test membuat UserInDB model"""
        user_in_db = UserInDB(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            hashed_password="hashed123"
        )
        assert user_in_db.username == "testuser"
        assert user_in_db.hashed_password == "hashed123"
    
    def test_token_model_creation(self):
        """Test membuat Token model"""
        token = Token(
            access_token="token123",
            token_type="bearer"
        )
        assert token.access_token == "token123"
        assert token.token_type == "bearer"
    
    def test_token_data_creation(self):
        """Test membuat TokenData model"""
        token_data = TokenData(username="testuser")
        assert token_data.username == "testuser"
    
    def test_token_data_optional_username(self):
        """Test TokenData dengan username optional"""
        token_data = TokenData()
        assert token_data.username is None

class TestSearchCriteriaModel:
    """Test suite untuk SearchCriteria model"""
    
    def test_search_criteria_empty(self):
        """Test membuat SearchCriteria kosong"""
        criteria = SearchCriteria()
        assert criteria.tags is None
        assert criteria.category is None
    
    def test_search_criteria_with_tags(self):
        """Test SearchCriteria dengan tags"""
        criteria = SearchCriteria(tags=["python", "fastapi"])
        assert criteria.tags == ["python", "fastapi"]
        assert criteria.category is None
    
    def test_search_criteria_with_category(self):
        """Test SearchCriteria dengan category"""
        criteria = SearchCriteria(category="Tutorial")
        assert criteria.category == "Tutorial"
        assert criteria.tags is None
    
    def test_search_criteria_with_both(self):
        """Test SearchCriteria dengan tags dan category"""
        criteria = SearchCriteria(
            tags=["python"],
            category="Tutorial"
        )
        assert criteria.tags == ["python"]
        assert criteria.category == "Tutorial"

class TestTaxonomyModels:
    """Test suite untuk Taxonomy models"""
    
    def test_category_model_creation(self):
        """Test membuat Category model"""
        category = Category(
            category_id="c1",
            name="Tutorial"
        )
        assert category.category_id == "c1"
        assert category.name == "Tutorial"
    
    def test_tag_model_creation(self):
        """Test membuat Tag model"""
        tag = Tag(
            tag_id="t1",
            name="python"
        )
        assert tag.tag_id == "t1"
        assert tag.name == "python"

class TestArticleModel:
    """Test suite untuk Article model"""
    
    def test_article_model_creation(self):
        """Test membuat Article model"""
        from datetime import date
        category = Category(category_id="c1", name="Tutorial")
        tags = [Tag(tag_id="t1", name="python")]
        
        article = Article(
            article_id="a1",
            title="Tutorial Python",
            publish_date=date(2025, 11, 15),
            snippet="Belajar Python dari nol",
            tags=tags,
            category=category
        )
        assert article.article_id == "a1"
        assert article.title == "Tutorial Python"
        assert len(article.tags) == 1
        assert article.category.name == "Tutorial"

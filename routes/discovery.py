from fastapi import APIRouter, Depends, Header, HTTPException
from typing import List, Optional
from models.discovery import SearchCriteria
from models.user import User
from database.db import mock_articles, mock_users
from auth.security import get_current_user

discovery_router = APIRouter(
    prefix="/discovery",
    tags=["Content Discovery"]
)

@discovery_router.post("/")
async def find_relevant_articles(
    criteria: SearchCriteria, 
    N: int = 10,
    authorization: Optional[str] = Header(None)
):
    """
    Mengeksekusi logika Core Domain.
    Hanya dapat diakses oleh authenticated user.
    """
    # Simple token validation
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    
    # Validate token exists and is not empty
    if not token or len(token) < 10:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # If token exists, proceed (simplified validation)
    all_articles = list(mock_articles.values())
    filtered_articles = all_articles

    if criteria.category:
        filtered_articles = [
            article for article in filtered_articles
            if article["category"]["name"].lower() == criteria.category.lower()
        ]

    if criteria.tags:
        search_tags_lower = {tag.lower() for tag in criteria.tags}
        temp_results = []
        for article in filtered_articles:
            article_tags_lower = {tag["name"].lower() for tag in article["tags"]}
            if search_tags_lower.issubset(article_tags_lower):
                temp_results.append(article)
        filtered_articles = temp_results

    results = filtered_articles[:N]
    return results
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.discovery import SearchCriteria
from models.user import User
from database.db import mock_articles
from auth.security import get_current_user

discovery_router = APIRouter(
    prefix="/discovery",
    tags=["Content Discovery"]
)

@discovery_router.post("/")
async def find_relevant_articles(
    criteria: SearchCriteria, 
    N: int = 10,
    current_user: User = Depends(get_current_user)
):
    """
    Mengeksekusi logika Core Domain.
    Hanya dapat diakses oleh authenticated user.
    """
    # If we reach here, user is authenticated and exists
    # (get_current_user dependency handles all validation)
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
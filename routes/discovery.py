from fastapi import APIRouter
from typing import List
from models.article import Article
from models.discovery import SearchCriteria
from database.db import mock_articles  

discovery_router = APIRouter(
    prefix="/discovery",
    tags=["Content Discovery"]
)

@discovery_router.post("/", response_model=List[Article])
async def find_relevant_articles(criteria: SearchCriteria, N: int = 10):
    results = []
    
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
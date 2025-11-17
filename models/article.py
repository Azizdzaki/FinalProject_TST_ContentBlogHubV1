from pydantic import BaseModel
from typing import List
from datetime import date
from .taxonomy import Tag, Category

class Article(BaseModel):
    article_id: str
    title: str
    publish_date: date
    snippet: str
    tags: List[Tag]      
    category: Category 
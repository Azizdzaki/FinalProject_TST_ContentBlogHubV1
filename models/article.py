from pydantic import BaseModel
from typing import List
from datetime import date
from .taxonomy import Tag, Category

class Article(BaseModel):
    """
    Entitas yang merepresentasikan sebuah Artikel.
    Sesuai Class Diagram [cite: 6255, 6296-6298].
    """
    article_id: str
    title: str
    publish_date: date
    snippet: str
    tags: List[Tag]      
    category: Category 
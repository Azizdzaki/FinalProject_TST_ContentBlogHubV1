from pydantic import BaseModel
from typing import List, Optional


class SearchCriteria(BaseModel):
    tags: Optional[List[str]] = None
    category: Optional[str] = None

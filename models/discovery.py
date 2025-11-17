from pydantic import BaseModel
from typing import List, Optional

class SearchCriteria(BaseModel):
    """
    Value Object yang merepresentasikan kriteria pencarian dari pengguna.
    Sesuai Class Diagram [cite: 6255, 6290-6291].
    """
    tags: Optional[List[str]] = None
    category: Optional[str] = None
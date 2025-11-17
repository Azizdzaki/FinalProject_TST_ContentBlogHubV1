from pydantic import BaseModel

class Tag(BaseModel):
    tag_id: str
    name: str

class Category(BaseModel):
    category_id: str
    name: str
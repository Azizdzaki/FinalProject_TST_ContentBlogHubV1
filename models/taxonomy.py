from pydantic import BaseModel

class Tag(BaseModel):
    """
    Entitas yang merepresentasikan sebuah Tag (label metadata spesifik).
    Sesuai Class Diagram[cite: 6255].
    """
    tag_id: str
    name: str

class Category(BaseModel):
    """
    Entitas yang merepresentasikan sebuah Category (topik utama).
    Sesuai Class Diagram[cite: 6255].
    """
    category_id: str
    name: str
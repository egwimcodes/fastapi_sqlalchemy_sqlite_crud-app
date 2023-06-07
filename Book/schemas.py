from pydantic import BaseModel, Field
from typing import Optional


class BookType(BaseModel):
    title: Optional[str] = Field(max_length=20)
    author: Optional[str] = Field(max_length=30)
    synopsis: Optional[str] = Field(min_length=1)
    published: Optional[int] = None

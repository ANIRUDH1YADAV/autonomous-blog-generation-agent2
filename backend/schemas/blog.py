from pydantic import BaseModel
from datetime import date


class BlogRequest(BaseModel):
    topic: str
    as_of: date


class BlogResponse(BaseModel):
    success: bool
    markdown: str
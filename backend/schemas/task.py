from pydantic import BaseModel, Field
from typing import List


class Task(BaseModel):
    id: int

    title: str

    goal: str = Field(
        ...,
        description="One sentence describing what the reader should do/understand."
    )

    bullets: List[str] 
        
     
    target_words: int = Field(
        ...,
        description="Target words (120–550)."
    )

    tags: List[str] = Field(default_factory=list)

    requires_research: bool = False

    requires_citations: bool = False

    requires_code: bool = False
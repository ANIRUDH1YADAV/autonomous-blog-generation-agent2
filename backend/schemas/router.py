from typing import List, Literal

from pydantic import BaseModel, Field


class RouterDecision(BaseModel):

    needs_research: bool

    mode: Literal[
        "closed_book",
        "hybrid",
        "open_book"
    ]

    reason: str

    queries: List[str] = Field(
        default_factory=list
    )

    max_results_per_query: int = Field(
        default=5
    )
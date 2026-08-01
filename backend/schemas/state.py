import operator

from typing import (
    TypedDict,
    List,
    Optional,
    Annotated
)

from schemas.plan import Plan
from schemas.evidence import EvidenceItem


class BlogState(TypedDict):

    topic: str

    mode: str

    needs_research: bool

    queries: List[str]

    evidence: List[EvidenceItem]

    plan: Optional[Plan]

    as_of: str

    recency_days: int

    sections: Annotated[
        List[tuple[int, str]],
        operator.add
    ]

    merged_md: str

    md_with_placeholders: str

    image_specs: List[dict]

    final: str
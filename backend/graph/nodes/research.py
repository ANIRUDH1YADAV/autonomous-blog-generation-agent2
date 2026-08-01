import os
from datetime import date, timedelta

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

from services.llm_service import LLMService
from schemas.state import BlogState
from schemas.evidence import EvidencePack


RESEARCH_SYSTEM = """
You are a research synthesizer.

Given raw web search results, produce EvidenceItem objects.

Rules:
- Only include items with a non-empty URL.
- Prefer relevant and authoritative sources.
- Normalize published_at to ISO YYYY-MM-DD if possible.
- Keep snippets short.
- Deduplicate by URL.
"""


def _tavily_search(query: str, max_results: int = 5):
    if not os.getenv("TAVILY_API_KEY"):
        return []

    tool = TavilySearchResults(max_results=max_results)
    results = tool.invoke({"query": query})

    out = []
    for r in results:
        out.append(
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("content") or r.get("snippet"),
                "published_at": r.get("published_date"),
                "source": r.get("source"),
            }
        )
    return out


def _iso_to_date(s):
    if not s:
        return None
    try:
        return date.fromisoformat(s[:10])
    except Exception:
        return None


def research_node(state: BlogState):
    llm = LLMService.get_llm()

    queries = (state.get("queries") or [])[:2]

    raw = []
    for q in queries:
        raw.extend(_tavily_search(q, max_results=2))

    if not raw:
        return {"evidence": []}

    extractor = llm.with_structured_output(EvidencePack)

    pack = extractor.invoke(
        [
            SystemMessage(content=RESEARCH_SYSTEM),
            HumanMessage(
                content=f"""
As-of date: {state['as_of']}
Recency days: {state['recency_days']}

Raw results:

{raw}
"""
            ),
        ]
    )

    dedup = {}
    for e in pack.evidence:
        if e.url:
            dedup[e.url] = e

    evidence = list(dedup.values())

    if state.get("mode") == "open_book":
        as_of = date.fromisoformat(state["as_of"])
        cutoff = as_of - timedelta(days=state["recency_days"])

        evidence = [
            e
            for e in evidence
            if (d := _iso_to_date(e.published_at)) and d >= cutoff
        ]

    return {"evidence": evidence}
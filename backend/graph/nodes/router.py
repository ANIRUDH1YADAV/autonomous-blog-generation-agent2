from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from schemas.router import RouterDecision
from schemas.state import BlogState

from services.llm_service import LLMService


ROUTER_SYSTEM = """
You are a routing module for a technical blog planner.

Decide whether web research is needed BEFORE planning.

Modes:

- closed_book (needs_research=false)
  Evergreen concepts that can be answered from general knowledge.

- hybrid (needs_research=true)
  Evergreen concepts that benefit from recent examples,
  frameworks, tools, benchmarks, or industry updates.

- open_book (needs_research=true)
  News, trends, latest developments, pricing changes,
  policy updates, product launches, weekly roundups.

Rules:

If needs_research=true:
- Generate between 3 and 10 focused search queries.
- Queries should be highly relevant to the topic.
- Avoid broad or generic searches.

If mode=open_book:
- Generate queries focused on the last 7 days.
- Prefer recent events and developments.

Return output strictly following RouterDecision schema.
"""


def router_node(state: BlogState):

    llm = LLMService.get_llm()

    decider = llm.with_structured_output(
        RouterDecision
    )

    decision = decider.invoke(
        [
            SystemMessage(
                content=ROUTER_SYSTEM
            ),
            HumanMessage(
                content=f"""
Topic: {state['topic']}
As-of date: {state['as_of']}
"""
            )
        ]
    )

    if decision.mode == "open_book":
        recency_days = 7

    elif decision.mode == "hybrid":
        recency_days = 45

    else:
        recency_days = 3650

    return {
        "needs_research": decision.needs_research,
        "mode": decision.mode,
        "queries": decision.queries,
        "recency_days": recency_days
    }


def route_next(state: BlogState):

    return (
        "research"
        if state["needs_research"]
        else "orchestrator"
    )
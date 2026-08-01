from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from services.llm_service import (
    LLMService
)

from schemas.plan import Plan
from schemas.state import BlogState


ORCH_SYSTEM = """
You are a senior technical writer and developer advocate.

Produce a highly actionable outline for a technical blog post.

Requirements:

- Produce 5–9 tasks.
- Each task must include:
  - title
  - goal
  - bullets
  - target_words

- Use evidence whenever available.

The execution mode is NOT the blog type.

Mode meanings:
- open_book: external evidence is available.
- hybrid: combine retrieved evidence with model knowledge.
- closed_book: rely only on model knowledge.

The field `blog_kind` MUST be EXACTLY one of:

- explainer
- tutorial
- news_roundup
- comparison
- system_design

Never invent a new blog_kind such as:
- hybrid
- mixed
- guide
- analysis
- research

Choose the closest valid value.

Examples:

Paper explanation -> explainer
Step-by-step implementation -> tutorial
Compare two approaches -> comparison
Recent developments -> news_roundup
Architecture deep dive -> system_design

Output must strictly follow the Plan schema.
"""


def orchestrator_node(state: BlogState):

    llm = LLMService.get_llm()

    planner = llm.with_structured_output(
        Plan
    )

    mode = state.get(
        "mode",
        "closed_book"
    )

    evidence = state.get(
        "evidence",
        []
    )

    forced_kind = (
        "news_roundup"
        if mode == "open_book"
        else None
    )

    plan = planner.invoke(
        [
            SystemMessage(
                content=ORCH_SYSTEM
            ),
            HumanMessage(
                content=(
                    f"Topic: {state['topic']}\n"
                    f"Mode: {mode}\n"
                    f"As-of: {state['as_of']}\n\n"
                    f"Evidence:\n"
                    f"{[e.model_dump() for e in evidence][:16]}"
                )
            )
        ]
    )

    if forced_kind:
        plan.blog_kind = forced_kind

    return {
        "plan": plan
    }
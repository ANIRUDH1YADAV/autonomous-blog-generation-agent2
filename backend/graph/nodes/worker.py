from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from services.llm_service import (
    LLMService
)

from schemas.task import Task
from schemas.plan import Plan
from schemas.evidence import EvidenceItem


WORKER_SYSTEM = """
You are a senior technical writer and developer advocate.

Write ONE section of a technical blog post in Markdown.

Rules:
- Cover all bullets.
- Output only markdown.
- Start with:

## Section Title

- Follow the target word count.
- Use evidence when provided.
- Include citations when required.
"""


def worker_node(payload: dict):

    llm = LLMService.get_llm()

    task = Task(**payload["task"])

    plan = Plan(**payload["plan"])

    evidence = [
        EvidenceItem(**e)
        for e in payload.get("evidence", [])
    ]

    bullets_text = "\n- " + "\n- ".join(
        task.bullets
    )

    evidence_text = "\n".join(
        [
            f"- {e.title} | {e.url}"
            for e in evidence[:3]
        ]
    )

    section_md = llm.invoke(
        [
            SystemMessage(
                content=WORKER_SYSTEM
            ),
            HumanMessage(
                content=(
                    f"Blog Title: {plan.blog_title}\n"
                    f"Topic: {payload['topic']}\n"
                    f"Section Title: {task.title}\n"
                    f"Goal: {task.goal}\n"
                    f"Target Words: {task.target_words}\n\n"
                    f"Bullets:\n{bullets_text}\n\n"
                    f"Evidence:\n{evidence_text}"
                )
            )
        ]
    ).content.strip()

    return {
        "sections": [
            (
                task.id,
                section_md
            )
        ]
    }
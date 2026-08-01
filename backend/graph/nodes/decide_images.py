from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from services.llm_service import (
    LLMService
)

from schemas.image import (
    GlobalImagePlan
)

from schemas.state import BlogState


DECIDE_IMAGES_SYSTEM = """
You are deciding which images should be generated for a blog post, and where they go.

You will be given the full blog markdown.

Your job:
1. Identify only valuable image opportunities — diagrams, architecture figures,
   workflows, and explanatory visuals. Avoid decorative or redundant images.
2. For each chosen image, create an ImageSpec with:
   - placeholder: a unique marker like "[[IMAGE_1]]", "[[IMAGE_2]]", etc.
   - filename: a short descriptive snake_case filename, e.g. "qkv_flow.png"
   - alt: concise alt text
   - caption: a short caption for the image
   - prompt: a detailed, descriptive text-to-image generation prompt
   - size and quality as appropriate
3. Take the ORIGINAL markdown and return it as `md_with_placeholders`, with each
   placeholder string inserted on its own line at the exact location in the text
   where that image should appear.
4. Do NOT remove, rewrite, or summarize any of the original text. Only insert the
   placeholder markers into it.
5. Every placeholder in `images` must appear exactly once in `md_with_placeholders`,
   and vice versa — no orphaned placeholders.
6. Return output strictly following the GlobalImagePlan schema.
"""


def decide_images(state: BlogState):

    llm = LLMService.get_llm()

    planner = llm.with_structured_output(
        GlobalImagePlan
    )

    image_plan = planner.invoke(
        [
            SystemMessage(
                content=DECIDE_IMAGES_SYSTEM
            ),
            HumanMessage(
                content=state.get(
                    "merged_md",
                    ""
                )
            )
        ]
    )

    return {
        "image_specs": image_plan.images,
        "md_with_placeholders": image_plan.md_with_placeholders
    }
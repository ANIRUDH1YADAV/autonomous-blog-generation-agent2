from fastapi import APIRouter
from graph.workflow import app

from schemas.blog import (
    BlogRequest,
    BlogResponse
)

router = APIRouter()


@router.post(
    "/generate",
   
)
async def generate_blog(
    request: BlogRequest
):

    result = app.invoke(
        {
            "topic": request.topic,
            "mode": "",
            "needs_research": False,
            "queries": [],
            "evidence": [],
            "plan": None,
            "as_of": str(request.as_of),
            "recency_days": 7,
            "sections": [],
            "merged_md": "",
            "md_with_placeholders": "",
            "image_specs": [],
            "final": "",
        }
    )

    print(result)

    return {
    "success": True,
    "markdown": result["final"],
    "plan": result["plan"],
    "evidence": result["evidence"],
    "image_specs": result["image_specs"],
    "logs": result
}
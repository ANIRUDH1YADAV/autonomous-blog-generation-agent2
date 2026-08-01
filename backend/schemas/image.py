from typing import List, Literal

from pydantic import BaseModel, Field


class ImageSpec(BaseModel):

    placeholder: str = Field(
        ...,
        description="[[IMAGE_1]]"
    )

    filename: str = Field(
        ...,
        description="qkv_flow.png"
    )

    alt: str

    caption: str

    prompt: str

    size: Literal[
        "1024x1024",
        "1024x1536",
        "1536x1024"
    ] = "1024x1024"

    quality: Literal[
        "low",
        "medium",
        "high"
    ] = "medium"


class GlobalImagePlan(BaseModel):

    md_with_placeholders: str

    images: List[ImageSpec] = Field(
        default_factory=list
    )
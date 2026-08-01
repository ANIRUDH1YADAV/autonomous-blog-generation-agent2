import os
from io import BytesIO
from pathlib import Path

from huggingface_hub import InferenceClient

GENERATED_IMAGES_DIR = Path(__file__).resolve().parent.parent / "generated_images"
GENERATED_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

HF_MODEL = "black-forest-labs/FLUX.1-dev"

QUALITY_STEPS = {
    "low": 15,
    "medium": 25,
    "high": 40,
}


class ImageService:

    _client = None

    @classmethod
    def get_client(cls) -> InferenceClient:
        if cls._client is None:
            token = os.environ.get("HF_TOKEN")
            if not token:
                raise RuntimeError(
                    "HF_TOKEN is not set in environment (.env)"
                )
            cls._client = InferenceClient(api_key=token)
        return cls._client

    @classmethod
    def generate_image(
        cls,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "medium",
    ) -> bytes:
        client = cls.get_client()

        width, height = map(int, size.split("x"))
        steps = QUALITY_STEPS.get(quality, 25)

        image = client.text_to_image(
            prompt,
            model=HF_MODEL,
            width=width,
            height=height,
            num_inference_steps=steps,
        )

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()

    @classmethod
    def save_image(cls, image_bytes: bytes, filename: str) -> str:
        if not filename.lower().endswith(".png"):
            filename = f"{filename}.png"
        path = GENERATED_IMAGES_DIR / filename
        with open(path, "wb") as f:
            f.write(image_bytes)
        return str(path)
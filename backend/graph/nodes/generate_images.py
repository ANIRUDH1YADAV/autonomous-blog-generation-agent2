from schemas.state import BlogState
from services.image_service import ImageService


def _get(spec, key, default=None):
    """Works whether spec is a pydantic ImageSpec or a plain dict."""
    if hasattr(spec, key):
        return getattr(spec, key)
    return spec.get(key, default)


def generate_and_place_images(state: BlogState):

    image_specs = state.get("image_specs", []) or []
    markdown = state.get("md_with_placeholders") or state.get("merged_md", "")

    for spec in image_specs:
        prompt = _get(spec, "prompt")
        size = _get(spec, "size", "1024x1024")
        quality = _get(spec, "quality", "medium")
        filename = _get(spec, "filename")
        placeholder = _get(spec, "placeholder")
        alt = _get(spec, "alt", "")
        caption = _get(spec, "caption", "")

        try:
            image_bytes = ImageService.generate_image(
                prompt=prompt,
                size=size,
                quality=quality,
            )
            saved_path = ImageService.save_image(image_bytes, filename)
        except Exception as exc:
            print(f"[generate_images] failed for '{placeholder}': {exc}")
            continue

        markdown_image = f"![{alt}]({saved_path})\n\n*{caption}*"
        markdown = markdown.replace(placeholder, markdown_image)

    return {
        "final": markdown
    }
import requests

BASE_URL = "http://localhost:8000"


def generate_blog(topic: str, as_of: str):

    response = requests.post(
        f"{BASE_URL}/api/blog/generate",
        json={
            "topic": topic,
            "as_of": as_of
        },
        timeout=600
    )

    response.raise_for_status()

    return response.json()  
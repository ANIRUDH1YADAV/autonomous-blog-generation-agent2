from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes.blog import router as blog_router

app = FastAPI(
    title="Autonomous Blog Generator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGES_DIR = Path(__file__).resolve().parent / "generated_images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/images",
    StaticFiles(directory=IMAGES_DIR),
    name="images"
)

app.include_router(
    blog_router,
    prefix="/api/blog",
    tags=["Blog"]
)


@app.get("/")
def root():
    return {
        "message": "Backend Running"
    }
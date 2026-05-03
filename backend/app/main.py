from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import init_db
from app.routers import analyze, cases
from app.schemas import HealthResponse


settings = get_settings()


def _find_public_dir() -> Path | None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "public"
        if candidate.exists() and candidate.is_dir():
            return candidate
    return None


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name)


app.include_router(analyze.router)
app.include_router(cases.router)

public_dir = _find_public_dir()
if public_dir:
    assets_dir = public_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/", include_in_schema=False)
    def root() -> FileResponse:
        return FileResponse(public_dir / "index.html")

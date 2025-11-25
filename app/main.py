import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import RedirectResponse

from app.core.database import init_db
from app.routers.auth import router as auth_router
from app.routers.detection import router as detection_router
from config import settings


def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(detection_router, prefix="/detection", tags=["detection"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    os.makedirs(settings.detection_upload_url, exist_ok=True)
    yield


app = FastAPI(lifespan=lifespan)
setup_cors(app)
setup_routers(app)


@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse(url="/docs")

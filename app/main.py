from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import RedirectResponse

from app.core.database import init_db
from app.core.detection import setup_model as setup_detection_model
from app.routers.auth import router as auth_router
from app.routers.detection import router as detection_router
from app.routers.exam import router as exam_router


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
    app.include_router(exam_router, prefix="/exam", tags=["exam"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    setup_detection_model()
    app.state.inference_store = {}
    yield
    app.state.inference_store.clear()


app = FastAPI(lifespan=lifespan)
setup_cors(app)
setup_routers(app)

app.mount("/data", StaticFiles(directory="data"), name="data")


@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse(url="/docs")

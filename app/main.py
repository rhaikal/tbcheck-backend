from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import init_db
from app.routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/")
def read_root():
    return {"message": "TBCheck API"}

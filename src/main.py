from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .database.connection import Base, engine
from .routers import orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()



app = FastAPI(lifespan=lifespan)
app.include_router(orders_router.router)


@app.exception_handler(Exception)
async def http_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    error = {
        "result": False,
        "error_type": exc.__class__.__name__,
        "error_message": exc.__str__(),
    }
    return JSONResponse(content=error)

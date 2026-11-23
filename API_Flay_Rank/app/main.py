from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routes import routes_tasks, meta_routes 


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app =FastAPI(lifespan=lifespan)

app.include_router(routes_tasks.router)
app.include_router(meta_routes.router)

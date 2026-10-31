from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database.core import engine, Base
from .entities.todo import Todo
from .entities.user import User
from .logging import configure_logging, LogLevels
from .api import register_routes

configure_logging(LogLevels.info)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("\n" + "=" * 55)
    print("🚀 Application successfully started!")
    print("👉 Swagger Docs:  http://localhost:8000/docs")
    print("👉 Alternative:   http://localhost:8000/redoc")
    print("=" * 55 + "\n", flush=True)
    yield

app = FastAPI(lifespan=lifespan)

register_routes(app)

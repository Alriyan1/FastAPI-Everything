from fastapi import FastAPI
from .database.core import engine,Base
from .entities.todo import Todo
from .entities.user import User
from .logging import configure_logging, LogLevels
from .api import register_routes

configure_logging(LogLevels.info)

app = FastAPI()

register_routes(app)
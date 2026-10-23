from fastapi import FastAPI
from .database.core import engine,Base
from .entities.todo import Todo
from .entities.user import User
from .api import register_routes

app = FastAPI()
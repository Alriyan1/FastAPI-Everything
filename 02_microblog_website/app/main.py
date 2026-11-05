from fastapi import FastAPI

from .app.database import engine
from .app.models import Base
from app.routes import users,auth,posts

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)
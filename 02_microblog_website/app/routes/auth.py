from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db

from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated

router = APIRouter(
    tags=["auth"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(auth.ACCESS_TOKEN_EXPIRE_MINUTES or 30))
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

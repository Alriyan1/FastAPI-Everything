from datetime import timedelta, datetime, timezone
from typing import Annotated
from uuid import UUID,uuid4
from fastapi import Depends

from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from sqlalchemy.orm import Session
from src.entities.user import User
from . import model
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from ..exceptions import AuthenticationError
import logging
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

auth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemas=['bcrypt'],deprecated='auto')

def verify_passward(plain_password:str,hashed_password:str)->bool:
    return bcrypt_context.verify(plain_password,hashed_password)

def get_password_hash(password:str)->str:
    return bcrypt_context.hash(password)

def authenticate_user(email:str,password:str,db:Session)->User|bool:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_passward(password,user.password_hash):
        logging.warning(f"Failed authentication attempt for email: {email}")
        return False
    return user

def create_access_token(email:str,user_id:UUID,expires_delta:timedelta)->str:
    encode = {
        'sub':email,
        "id":str(user_id),
        "exp":datetime.now(timezone.utc)+expires_delta
    }
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_token(token:str)->model.TokenData:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("id")
        return model.TokenData(user_id=user_id)
    except PyJWTError as e:
        logging.error(f"JWT verification failed: {e}")
        raise AuthenticationError()

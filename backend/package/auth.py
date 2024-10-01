"""########################################################################################
Name: auth.py
Description: This script contains a handful of useful authentication functions
Imports:
"""

from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import HTTPException
from jose import jwt

from .db import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, DB_COLLECTIONS, SECRET_KEY
from .globals import LOGGER
from .routes.user.models import *

"""
########################################################################################"""

"""
No need for these two functions (inside is jsut a single function)

def verify_password(plain_password, hashed_password):
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)

def get_password_hash(password):
    return PASSWORD_CONTEXT.hash(password)
"""


def create_access_token(data: TokenData) -> str:
    to_encode = data.model_dump()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_from_token(token: str) -> UserInDB:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user = DB_COLLECTIONS["users"].find_one({"username": username})
        user = UserInDB(**user, id=str(user["_id"]))
        return user
    except Exception as e:
        LOGGER.error(f"Error decoding token: {e}")
        raise HTTPException(status_code=400, detail="Could not validate credentials")


def authenticate_user(username: str, password: str) -> UserInDB:
    user = UserInDB(**DB_COLLECTIONS["users"].find_one({"username": username}))
    if not user:
        return False
    if not bcrypt.checkpw(
        password.encode("utf-8"), user.hashed_password.encode("utf-8")
    ):
        return False
    return user

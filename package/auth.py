"""########################################################################################
Name: auth.py
Description: This script contains a handful of useful authentication functions
Imports:
"""

from datetime import datetime, timezone, timedelta

from jose import jwt

from fastapi import HTTPException

from .globals import LOGGER
from .db import DB_COLLECTIONS, PASSWORD_CONTEXT, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from .routes.user.models import *

"""
########################################################################################"""

'''
No need for these two functions (inside is jsut a single function)

def verify_password(plain_password, hashed_password):
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)

def get_password_hash(password):
    return PASSWORD_CONTEXT.hash(password)
'''


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
        user["id"] = str(user["_id"])
        user = UserInDB(**DB_COLLECTIONS["users"].find_one({"username": username}))
        return user
    except Exception as e:
        LOGGER.error(f"Error decoding token: {e}")
        raise HTTPException(
            status_code=400, detail="Could not validate credentials"
        )

def authenticate_user(username: str, password: str) -> UserInDB:
    user = UserInDB(**DB_COLLECTIONS["users"].find_one({"username": username}))
    if not user:
        return False
    if not PASSWORD_CONTEXT.verify(password, user.hashed_password):
        return False
    return user


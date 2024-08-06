"""########################################################################################
Name: user/functions.py
Description: 
Imports:
"""

from bson import ObjectId
from fastapi import HTTPException

from ...globals import DB_COLLECTIONS, LOGGER, PASSWORD_CONTEXT
from .models import *

"""
########################################################################################"""


async def add_user(user: UserForEdit) -> User:
    user_for_db = UserInDB(**user.model_dump())
    user_for_db.hashed_password = PASSWORD_CONTEXT.hash(user.password)
    DB_COLLECTIONS["users"].insert_one(user_for_db.model_dump())
    return User(**user.model_dump())


async def get_user(user_id: int | str) -> User:
    user = DB_COLLECTIONS["users"].find_one({"_id": ObjectId(user_id)})
    return User(**user)


async def update_user(user_id: int | str, user: UserForEdit) -> User:
    if ObjectId(user_id) != user.get("_id", ""):
        LOGGER.error("User ID does not match the ID in the user object.")
        return HTTPException(
            status_code=400, detail="User ID does not match the ID in the user object"
        )

    user_to_edit = DB_COLLECTIONS["users"].find_one({"_id": ObjectId(user_id)})
    user_to_edit.update(User(user.model_dump()))
    if user.get("password"):
        user_to_edit["hashed_password"] = PASSWORD_CONTEXT.hash(user.password)

    DB_COLLECTIONS["users"].update_one({"_id": user.get("_id", "")}, user_to_edit)
    return User(**user_to_edit)


async def delete_user(user_id: int) -> User:
    user = DB_COLLECTIONS["users"].find_one({"_id": user_id})
    DB_COLLECTIONS["users"].delete_one({"_id": user_id})
    return User(**user)

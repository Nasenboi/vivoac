"""########################################################################################
Name: user/functions.py
Description: 
Imports:
"""

from typing import List, Union

from bson import ObjectId
from fastapi import HTTPException

from ...db import DB_COLLECTIONS, PASSWORD_CONTEXT
from ...globals import LOGGER
from .models import *

"""
########################################################################################"""


async def add_user(user: UserForEdit) -> User:
    user_for_db = UserInDB(**user.model_dump())
    user_for_db.hashed_password = PASSWORD_CONTEXT.hash(user.password)

    # check if user with this exact full_name already exists
    if DB_COLLECTIONS["users"].find_one({"username": user_for_db.username}):
        LOGGER.error("User with this username already exists.")
        return HTTPException(
            status_code=400, detail="User with this username already exists."
        )

    DB_COLLECTIONS["users"].insert_one(user_for_db.model_dump())
    return User(**user.model_dump())


async def get_user(user: User) -> Union[User, List[User]]:
    query = {k: v for k, v in user.model_dump().items() if v is not None}

    try:
        users = list(DB_COLLECTIONS["users"].find(query))

        if len(users) == 1:
            return User(**users[0])
        else:
            return [User(**user) for user in users]
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found.")


async def update_user(user_id: Union[int, str], user: UserForEdit) -> User:
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

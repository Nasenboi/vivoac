"""########################################################################################
Name: user/functions.py
Description: 
Imports:
"""

from typing import List, Union

import bcrypt
from bson import ObjectId
from fastapi import HTTPException

from ...db import DB_COLLECTIONS
from ...globals import LOGGER
from .models import *

"""
########################################################################################"""


async def get_user(user_id: PydanticObjectId = None) -> User:
    try:
        user = DB_COLLECTIONS["users"].find_one({"_id": user_id})

        if not user:
            raise Exception("User not found")

        user = User.model_validate(user)
    except Exception as e:
        LOGGER.error(f"Error getting user: {e}")
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def find_users(user_query: dict = {}) -> List[User]:
    try:
        query = {
            k: v
            for k, v in user_query.items()
            if v is not None and k not in ["_id", "created_at", "updated_at"]
        }
        users = list(DB_COLLECTIONS["users"].find(query))
    except Exception as e:
        LOGGER.error(f"Error finding users: {e}")
        raise HTTPException(status_code=404, detail="Users not found")
    return [User.model_validate(user) for user in users]


async def create_user(user: UserForEdit) -> UserForEdit:
    try:
        # check if there are any Users with the same name:
        users = await find_users(
            user_query={
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )
        if len(users) > 0:
            raise HTTPException(
                status_code=400,
                detail="A User this name does with already exists",
            )

        user_for_db = UserInDB(
            **user.model_dump(exclude_unset=True, exclude={"password"})
        )
        user_for_db.hashed_password = bcrypt.hashpw(
            user.password.encode("utf-8"), bcrypt.gensalt()
        )

        # insert User
        user_id = (
            DB_COLLECTIONS["users"].insert_one(user_for_db.model_dump()).inserted_id
        )
        user = await get_user(user_id)
    except Exception as e:
        LOGGER.error(f"Error creating User: {e}")
        raise HTTPException(status_code=500, detail="Error creating User")
    return user


async def update_user(user_id: str, user: User) -> User:
    try:
        user_update = user.model_dump(
            exclude_unset=True, exclude={"_id", "created_at", "updated_at"}
        )

        # update User
        DB_COLLECTIONS["users"].update_one({"_id": user_id}, {"$set": user_update})
        user = await get_user(user_id=user_id)
    except Exception as e:
        LOGGER.error(f"Error updating User: {e}")
        raise HTTPException(status_code=500, detail="Error updating User")
    return user


async def delete_user(user_id: PydanticObjectId) -> User:
    try:
        # check if User exists and fetch it
        user = await get_user(user_id=user_id)
        # delete User
        DB_COLLECTIONS["users"].delete_one({"_id": user_id})
    except Exception as e:
        LOGGER.error(f"Error deleting User: {e}")
        raise HTTPException(status_code=500, detail="Error deleting User")
    return user

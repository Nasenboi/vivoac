"""########################################################################################
Name: db.py
Description: This script will setup the mongo database and create the defaut admin user,
if it does not exist.
Imports:
"""

import json
import os
from typing import Dict

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pymongo import MongoClient
from pymongo.collection import Collection

from .globals import LOGGER, SETTINGS_GLOBAL
from .routes.user.models import User

"""
########################################################################################"""


ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

# Create the client for the mongo database:
DB_CLIENT = MongoClient(
    SETTINGS_GLOBAL.get("database", {}).get("url", None),
    username=ADMIN_USER,
    password=ADMIN_PASSWORD,
)
db_name = SETTINGS_GLOBAL.get("database", {}).get("collection", "vivoac")
VIVOAC_DB = DB_CLIENT[db_name]

# Initialize and create the collections if they dont exist:
DB_COLLECTIONS: Dict[str, Collection] = {
    "sessions": None,
    "users": None,
    "voices": None,
    "voice_talents": None,
}
for collection in DB_COLLECTIONS.keys():
    DB_COLLECTIONS[collection] = VIVOAC_DB[collection]


SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32))
ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = SETTINGS_GLOBAL.get("authentication", {}).get("access_token_expire_minutes", 30),
PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH_2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")

# Create the admin user for the db if it does not exist
if not DB_COLLECTIONS["users"].find_one({"username": ADMIN_USER}):
    admin_user: dict = User(
        username=ADMIN_USER,
        full_name="admin",
        role="admin",
        disabled=False,
    ).model_dump()
    admin_user["hashed_password"] = PASSWORD_CONTEXT.hash(ADMIN_PASSWORD)
    DB_COLLECTIONS["users"].insert_one(admin_user)
    LOGGER.info("Created the admin user in the database.")

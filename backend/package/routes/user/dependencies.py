"""########################################################################################
Name: user/dependencies.py
Description: These are authentication dependencies.
The user will send a token based on the OpenAPI specs and FastAPI will fetch the user and
their permissions.

TODO - maybe use just the informations inside of the jws token (remove id and add role to TokenData)
Imports:
"""

from fastapi import Depends, HTTPException, status

from...db import OAUTH_2_SCHEME
from ...auth import get_user_from_token

from .models import *

"""
########################################################################################"""

def get_current_user(token: str = Depends(OAUTH_2_SCHEME)) -> User:
    user = User(**get_user_from_token(token).model_dump())
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return current_user


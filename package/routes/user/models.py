"""########################################################################################
Name: user/models.py
Description: 
Imports:
"""

from typing import Optional

from pydantic import BaseModel, EmailStr

"""
########################################################################################"""


class User(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    disabled: Optional[bool] = None


class UserForEdit(User):
    password: Optional[str] = None


class UserInDB(User):
    hashed_password: Optional[str] = None

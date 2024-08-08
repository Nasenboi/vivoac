"""########################################################################################
Name: user/models.py
Description: 
Imports:
"""

from typing import Literal, Optional, Union

from pydantic import BaseModel, EmailStr

"""
########################################################################################"""


class User(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Literal["admin", "user"]] = "user"
    disabled: Optional[bool] = False


class UserForEdit(User):
    password: Optional[str] = None


class UserInDB(User):
    hashed_password: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    id: Union[int, str] = None

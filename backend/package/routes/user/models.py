"""########################################################################################
Name: user/models.py
Description: 
Imports:
"""

from typing import Literal, Optional, Union

from pydantic import BaseModel, EmailStr, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from ...utils.models import Address, CreatedUpdatedAt

"""
########################################################################################"""


class User(BaseModel, CreatedUpdatedAt):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Literal["admin", "user"]] = None
    address: Optional[Address] = None
    phone_number_home: Optional[PhoneNumber] = None
    phone_number_mobile: Optional[PhoneNumber] = None
    disabled: Optional[bool] = None


class UserForEdit(User):
    password: Optional[str] = None


class UserInDB(User):
    hashed_password: Optional[str] = None
    id: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    id: Union[int, str] = None

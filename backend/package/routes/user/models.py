"""########################################################################################
Name: user/models.py
Description: 
Imports:
"""

from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from ...utils.models import Address, CreatedUpdatedAt, PydanticObjectId
from ..audio.models import Audio_Format

"""
########################################################################################"""


class User_Config(BaseModel):
    audio_format: Optional[Audio_Format] = None


class User(BaseModel, CreatedUpdatedAt):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Literal["admin", "user"]] = None
    address: Optional[Address] = None
    phone_number_home: Optional[PhoneNumber] = None
    phone_number_mobile: Optional[PhoneNumber] = None
    disabled: Optional[bool] = None
    config: Optional[User_Config] = User_Config()


# -- Query Model --
# Ignore all fields that do not fit into a query
class User_Query(User):
    config: None = None
    address: None = None


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

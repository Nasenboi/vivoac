"""########################################################################################
Name: voice_talent/models.py
Description: 
Imports:
"""

from typing import Literal, Optional, Union

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from ...utils.models import Address, CreatedUpdatedAt, PydanticObjectId
from .functions import *

"""
########################################################################################"""


class Voice_Talent(BaseModel, CreatedUpdatedAt):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    voices: Optional[list[str]] = None
    birth_date: Optional[str] = None
    gender: Optional[
        Union[Literal["male", "female", "transgender", "non-binary"], str]
    ] = None
    address: Optional[Address] = None
    phone_number_home: Optional[PhoneNumber] = None
    phone_number_mobile: Optional[PhoneNumber] = None


# -- Query Model --
# Ignore all fields that do not fit into a query
class Voice_Talent_Query(Voice_Talent):
    voices: None = None
    address: None = None

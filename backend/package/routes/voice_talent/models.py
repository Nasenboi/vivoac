"""########################################################################################
Name: voice_talent/models.py
Description: 
Imports:
"""

from typing import Literal, Optional, Union

from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from ...utils.models import Address, CreatedUpdatedAt

"""
########################################################################################"""


class Voice_Talent(BaseModel, CreatedUpdatedAt):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    voices: Optional[list[str]] = None
    birth_date: Optional[str] = None
    gender: Optional[
        Union[Literal["male", "female", "transgender", "non-binary"], str]
    ] = None
    address: Optional[Address] = None
    phone_number_home: Optional[PhoneNumber] = None
    phone_number_mobile: Optional[PhoneNumber] = None

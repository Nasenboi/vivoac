"""########################################################################################
Name: http_models/parameters.py
Description: In here are some dependency functions that will be used for http request parameters.
Imports:
"""

from pydantic import BaseModel
from ..routes.user.models import User

from typing import Generic, TypeVar, Optional
from ..globals import SETTINGS_GLOBAL

"""
########################################################################################"""


class VivoacBaseHeader(BaseModel):
    api_version: str
    session_id: str
    api_key: Optional[str] = None
    user: Optional[User] = None


T = TypeVar("T")


class VivoacBaseResponse(BaseModel, Generic[T]):
    api_version: str = SETTINGS_GLOBAL.get("metadata", {}).get("api_version", "0.0.0")
    session_id: Optional[str] = None
    data: Optional[T] = None

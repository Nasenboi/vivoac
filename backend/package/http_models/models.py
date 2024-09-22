"""########################################################################################
Name: http_models/parameters.py
Description: In here are some dependency functions that will be used for http request parameters.
Imports:
"""

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

from ..globals import SETTINGS_GLOBAL
from ..routes.user.models import User

"""
########################################################################################"""


class VivoacBaseHeader(BaseModel):
    api_version: str
    api_key: Optional[str] = None
    user: Optional[User] = None


T = TypeVar("T")


class VivoacBaseResponse(BaseModel, Generic[T]):
    api_version: str = SETTINGS_GLOBAL.get("metadata", {}).get("api_version", "0.0.0")
    data: Optional[T] = None

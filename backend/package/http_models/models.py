"""########################################################################################
Name: http_models/parameters.py
Description: In here are some dependency functions that will be used for http request parameters.
Imports:
"""

from pydantic import BaseModel
from ..routes.user.models import User

from typing import Optional

"""
########################################################################################"""


class VivoacBaseHeader(BaseModel):
    api_version: str
    session_id: str
    api_key: Optional[str] = None
    user: Optional[User] = None

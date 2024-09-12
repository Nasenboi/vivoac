"""########################################################################################
Name: http_models/parameters.py
Description: In here are some dependency functions that will be used for http request parameters.
Imports:
"""

from fastapi import Header, Depends, HTTPException, status
from typing import Optional, Annotated
from packaging.version import Version

from pydantic import BaseModel
from ..routes.user.models import User
from ..routes.user.dependencies import get_admin_user, get_current_user

from ..globals import SETTINGS_GLOBAL
from .models import VivoacBaseHeader

"""
########################################################################################"""


async def check_api_version(api_version: Annotated[str, Header()]) -> str:
    min_version = SETTINGS_GLOBAL.get("metadata", {}).get("api_min_version", "0.0.0")
    if Version(api_version) < Version(min_version):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"API version {api_version} is not supported. Minimum version is {min_version}",
        )

def get_vivoac_base_header_dependency(
    get_user=True, get_api_key=False, check_admin=False
) -> function:
    params = {
        "session_id": Annotated[str, Header()],
        "api_version": Annotated[str, check_api_version()],
    }
    if get_user:
        if check_admin:
            params["user"] = Annotated[User, Depends(get_admin_user)]
        else:
            params["user"] = Annotated[User, Depends(get_current_user)]

    if get_api_key:
        params["api_key"] = Annotated[str, Header()]

    async def dependency(**kwargs):
        return VivoacBaseHeader(**kwargs)

    return dependency

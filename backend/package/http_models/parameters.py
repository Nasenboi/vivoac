"""########################################################################################
Name: http_models/parameters.py
Description: In here are some dependency functions that will be used for http request parameters.
Imports:
"""

from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from packaging.version import Version

from ..globals import SETTINGS_GLOBAL
from ..routes.user.dependencies import get_admin_user, get_current_user
from ..routes.user.models import User
from .models import VivoacBaseHeader

"""
########################################################################################"""


def empty_dependency():
    return None


async def check_api_version(api_version: str = Header()) -> str:
    min_version = SETTINGS_GLOBAL.get("metadata", {}).get("api_min_version", "0.0.0")
    if Version(api_version) < Version(min_version):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"API version {api_version} is not supported. Minimum version is {min_version}",
        )
    return api_version


def get_vivoac_base_header_dependency(
    get_user=True, get_api_key=False, check_admin=False
) -> VivoacBaseHeader:
    if get_user:
        if check_admin:
            user = Depends(get_admin_user)
        else:
            user = Depends(get_current_user)
    else:
        user = empty_dependency

    api_key = Header() if get_api_key else Depends(empty_dependency)

    async def dependency(
        api_version: str = Depends(check_api_version),
        user: Optional[User] = user,
        api_key: Optional[str] = api_key,
    ) -> VivoacBaseHeader:
        return VivoacBaseHeader(api_version=api_version, user=user, api_key=api_key)

    return dependency

"""########################################################################################
Name: session/routes.py
Description: 
Imports:
"""

from fastapi import APIRouter

"""
########################################################################################"""

session_router = APIRouter(
    prefix="/session",
    tags=["session"],
    responses={404: {"description": "Not found"}},
)

"""########################################################################################
Name: ai_api_handler/routes.py
Description: 
Imports:
"""

from fastapi import APIRouter

"""
########################################################################################"""

ai_api_handler_router = APIRouter(
    prefix="/ai_api_handler",
    tags=["ai_api_handler"],
    responses={404: {"description": "Not found"}},
)

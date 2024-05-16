"""########################################################################################
Name: audio/routes.py
Description: 
Imports:
"""

from fastapi import APIRouter

"""
########################################################################################"""

audio_router = APIRouter(
    prefix="/audio",
    tags=["audio"],
    responses={404: {"description": "Not found"}},
)

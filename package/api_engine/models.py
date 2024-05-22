"""########################################################################################
Name: api_engine/models.py
Description: 
Imports:
"""

from typing import Optional, Union
from uuid import uuid4

from pydantic import BaseModel

from ..routes.audio.models import Audio_Format

"""
########################################################################################"""


########################################################################################
# Session Models


class SessionSettings(BaseModel):
    audio_format: Audio_Format = Audio_Format()


class Session(BaseModel):
    sesstion_settings: Optional[SessionSettings] = SessionSettings()
    session_id: Optional[str] = uuid4()

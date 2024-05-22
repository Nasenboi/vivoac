"""########################################################################################
Name: script/models.py
Description: In here are the dictionary models that will be used for the script routes.
Imports:
"""

from typing import Optional
from uuid import uuid4

from pydantic import BaseModel

from ..audio.models import Audio_Format

"""
########################################################################################"""


class SessionSettings(BaseModel):
    audio_format: Audio_Format = Audio_Format()


class Session(BaseModel):
    sesstion_settings: Optional[SessionSettings] = SessionSettings()
    session_id: Optional[str] = uuid4()

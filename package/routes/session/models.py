"""########################################################################################
Name: script/models.py
Description: 
Imports:
"""

from typing import Optional
from uuid import uuid4

from pydantic import BaseModel

from ..audio.models import Audio_Format
from .engine_backend.models import *

"""
########################################################################################"""


class Session_Settings(BaseModel):
    audio_format: Optional[Audio_Format] = None

    def fill_default_values(self):
        self.audio_format = self.audio_format or Audio_Format().fill_default_values()
        return self


class Session(BaseModel):
    session_settings: Optional[Session_Settings] = None
    api_engine_modules: Optional[API_Sub_Engines] = None
    session_id: Optional[str] = None

    def fill_default_values(self):
        self.session_settings = (
            self.session_settings or Session_Settings().fill_default_values()
        )
        self.session_id = self.session_id or str(uuid4())
        return self

"""########################################################################################
Name: script/models.py
Description: 
Imports:
"""

from fastapi import Depends

from typing import Optional
from uuid import uuid4

from datetime import datetime

from pydantic import BaseModel, Field

from ..audio.models import Audio_Format

"""
########################################################################################"""


class Session_Settings(BaseModel):
    audio_format: Optional[Audio_Format] = None

    @staticmethod
    def query_extractor(audio_format: Audio_Format = Depends()):
        return Session_Settings(audio_format=audio_format)

    def fill_default_values(self):
        self.audio_format = self.audio_format or Audio_Format().fill_default_values()
        return self


class Session(BaseModel):
    session_settings: Optional[Session_Settings] = None
    session_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    @staticmethod
    def query_extractor(
        session_id: Optional[str] = None,
        session_settings: Session_Settings = Depends(Session_Settings.query_extractor),
    ):
        return Session(session_id=session_id, session_settings=session_settings)

    def update(self, new_session: BaseModel):
        self.session_settings = new_session.session_settings or self.session_settings
        return self

    def fill_default_values(self):
        self.session_settings = (
            self.session_settings or Session_Settings().fill_default_values()
        )
        self.session_id = self.session_id or str(uuid4())
        return self

"""########################################################################################
Name: ai_api_handler/models.py
Description: 
Imports:
"""

from typing import Annotated, List, Optional, Union

from pydantic import BaseModel

"""
########################################################################################"""


class VoiceSettings(BaseModel):
    voice_id: str | int = None
    name: str = None
    settings: dict = None
    description: Optional[str] = None
    files: Optional[List[str]] = None
    labels: Optional[dict] = None


class TextToSpeech(BaseModel):
    text: str = None
    voice: str = None
    voice_settings: VoiceSettings = None
    model: Optional[str] = None
    seed: Optional[int] = -1

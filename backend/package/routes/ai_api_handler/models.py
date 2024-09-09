"""########################################################################################
Name: ai_api_handler/models.py
Description: 
Imports:
"""

from typing import Annotated, List, Optional, Union

from pydantic import BaseModel

"""
########################################################################################"""


class Voice_Settings(BaseModel):
    voice_id: str = None
    name: str = None
    settings: dict = None
    description: Optional[str] = None
    files: Optional[List[str]] = None
    labels: Optional[dict] = None


class Text_To_Speech(BaseModel):
    text: str = None
    voice: str = None
    voice_settings: Optional[Voice_Settings] = None
    model: Optional[str] = None
    seed: Optional[int] = -1

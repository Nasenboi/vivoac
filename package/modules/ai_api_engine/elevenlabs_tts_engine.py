"""########################################################################################
Name: elevenlabs_tts_engine.py
Description: 

Imports:
"""

import os
from io import BytesIO
from typing import List

from pydub import AudioSegment

from ...base_classes.ai_api_engine import AI_API_Engine
from ...routes.ai_api_handler.models import *
from ...routes.audio.models import *

"""
########################################################################################"""


class ElevenLabs_TTS_Engine(AI_API_Engine):
    # class variables:

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        super().__init__(api_key=api_key, base_url=base_url, model=model)

        pass

    ############################################################
    # getter functions:

    def get_user_data(self, api_key: str = None) -> dict:
        pass

    def get_models(self, api_key: str = None) -> List[str]:
        pass

    def get_voices(self, api_key: str = None) -> List[str]:
        pass

    def get_character_voice(self, api_key: str = None, name: str = None) -> str:
        pass

    def get_voice_settings(
        self, api_key: str = None, voice_id: str = None
    ) -> Voice_Settings:
        pass

    ############################################################
    # Voice editing functions:

    def create_voice(
        self,
        api_key: str = None,
        voice_settings: Voice_Settings = None,
    ) -> str:
        pass

    def edit_voice_settings(
        self,
        api_key: str = None,
        voice_settings: Voice_Settings = None,
    ) -> None:
        pass

    def delete_voice(self, api_key: str = None, voice_id: str = None) -> None:
        pass

    ############################################################
    # Text to Speech

    def text_to_speech(
        self,
        api_key: str = None,
        text: str = None,
        voice: str = None,
        voice_settings: Voice_Settings = None,
        model: str = None,
        seed: int = None,
        audio_format: Audio_Format = None,
    ) -> bytes:
        pass

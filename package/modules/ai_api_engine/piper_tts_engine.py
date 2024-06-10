"""########################################################################################
Name: ai_api_engine/piper_tts_engine.py
Description: The base class for all AI API Engine classes
Most of the functions are build after the ElevenLabs API but can be adapted to other APIs,
because thats what the modular child classes are for!
Imports:
"""

from typing import List

from ...base_classes import AI_API_Engine

"""
########################################################################################"""


class Piper_TTS_Engine(AI_API_Engine):
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

    def get_voice_settings(self, api_key: str = None, voice_id: str = None) -> dict:
        pass

    ############################################################
    # Voice editing functions:

    def create_voice(
        self,
        api_key: str = None,
        name: str = None,
        description: str = None,
        files: List[str] = None,
        labels: dict = None,
    ) -> str:
        pass

    def edit_voice_settings(
        self,
        api_key: str = None,
        voice_id: str = None,
        name: str = None,
        description: str = None,
        files: List[str] = None,
        labels: dict = None,
        settings: dict = None,
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
        voice_settings: dict = None,
        model: str = None,
        seed: int = None,
    ) -> bytes:
        pass

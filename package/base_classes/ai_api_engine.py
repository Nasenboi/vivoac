"""########################################################################################
Name: base_classes/ai_api_engine.py
Description: The base class for all AI API Engine classes
Most of the functions are build after the ElevenLabs API but can be adapted to other APIs,
because thats what the modular child classes are for!
Imports:
"""

from typing import List

from ..utils.decorators import virtual
from .base_engine import Base_Engine

"""
########################################################################################"""


class AI_API_Engine(Base_Engine):
    # class variables:
    api_key: str = None  # the api token or key to use the service
    base_url: str = None  # the base url of the api
    model: str = None  # the model to use for the api

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        pass

    ############################################################
    # getter functions:

    @virtual
    def get_user_data(self, api_key: str = None) -> dict:
        pass

    @virtual
    def get_models(self, api_key: str = None) -> List[str]:
        pass

    @virtual
    def get_voices(self, api_key: str = None) -> List[str]:
        pass

    @virtual
    def get_character_voice(self, api_key: str = None, name: str = None) -> str:
        pass

    @virtual
    def get_voice_settings(self, api_key: str = None, voice_id: str = None) -> dict:
        pass

    ############################################################
    # Voice editing functions:

    @virtual
    def create_voice(
        self,
        api_key: str = None,
        name: str = None,
        description: str = None,
        files: List[str] = None,
        labels: dict = None,
    ) -> str:
        pass

    @virtual
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

    @virtual
    def delete_voice(self, api_key: str = None, voice_id: str = None) -> None:
        pass

    ############################################################
    # Text to Speech

    @virtual
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

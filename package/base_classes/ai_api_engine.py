"""########################################################################################
Name: base_classes/ai_api_engine.py
Description: The base class for all AI API Engine classes
Most of the functions are build after the ElevenLabs API but can be adapted to other APIs,
because thats what the modular child classes are for!
Imports:
"""

import os
from io import BytesIO
from typing import List

from pydub import AudioSegment

from ..routes.ai_api_handler.models import *
from ..routes.audio.models import *
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
        voice_settings: Voice_Settings = None,
        model: str = None,
        seed: int = None,
        audio_format: Audio_Format = None,
    ) -> bytes:
        pass

    ############################################################
    # Constant audio helper functions:

    def apply_audio_format(
        self,
        target_format: Audio_Format,
        audio_file_name: str = "",
        audio_file: bytes = None,
    ) -> str | bytes:
        target_format.fill_default_values()

        # Load the audio file
        if audio_file_name:
            audio = AudioSegment.from_file(audio_file_name)
        elif audio_file:
            audio = AudioSegment.from_file(BytesIO(audio_file))
        else:
            raise ValueError("No audio file provided")

        # Apply normalization if needed
        if target_format.normalization_type == "Peak":
            audio = audio.apply_gain(-audio.max_dBFS)
        elif target_format.normalization_type == "Loudness":
            audio = audio.normalize()

        # Convert to target format
        audio = audio.set_frame_rate(target_format.sample_rate)
        audio = audio.set_channels(target_format.channels)
        audio = audio.set_sample_width(target_format.bit_depth // 8)

        # Export the audio
        output = BytesIO()

        if audio_file_name:
            new_file_name = audio_file_name.replace(
                audio_file_name.split(".")[-1], target_format.codec
            )
            audio.export(new_file_name, format=target_format.codec)
            # remove old file
            if new_file_name != audio_file_name:
                os.remove(audio_file_name)
            return new_file_name
        else:
            audio.export(
                output, format=target_format.codec, bitrate=f"{target_format.bit_rate}k"
            )
            return output.getvalue()

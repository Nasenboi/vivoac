"""########################################################################################
Name: voice/functions.py
Description: 
Imports:
"""

from datetime import datetime
from typing import List

from fastapi import HTTPException

from ...api_engine.api_engine_base import API_Engine_Base
from ...db import DB_COLLECTIONS
from ...globals import LOGGER
from ...utils.models import PydanticObjectId
from ..voice_talent.functions import get_voice_talent
from .models import Voice, Voice_Map

"""
########################################################################################"""


async def get_voice(voice_id: PydanticObjectId = None) -> Voice:
    try:
        voice = DB_COLLECTIONS["voices"].find_one({"_id": voice_id})

        if not voice:
            raise Exception("Voice not found")

        voice = Voice.model_validate(voice)
    except Exception as e:
        LOGGER.error(f"Error getting voice: {e}")
        raise HTTPException(status_code=404, detail="Voice not found")
    return voice


async def find_voices(voice_query: dict = {}) -> List[Voice]:
    try:
        query = {
            k: v
            for k, v in voice_query.items()
            if v is not None and k not in ["_id", "created_at", "updated_at"]
        }
        voices = list(DB_COLLECTIONS["voices"].find(query))
    except Exception as e:
        LOGGER.error(f"Error finding voices: {e}")
        raise HTTPException(status_code=404, detail="Voices not found")
    return [Voice.model_validate(voice) for voice in voices]


async def create_voice(voice: Voice) -> Voice:
    try:
        # check if there are any voices with the same name:
        voices = await find_voices(
            voice_query={
                "first_name": voice.first_name,
                "last_name": voice.last_name,
            }
        )
        if len(voices) > 0:
            raise HTTPException(
                status_code=400,
                detail="A voice this name does with already exists",
            )

        # insert voice
        voice_id = DB_COLLECTIONS["voices"].insert_one(voice.model_dump()).inserted_id
        voice = await get_voice(voice_id)
    except Exception as e:
        LOGGER.error(f"Error creating voice: {e}")
        raise HTTPException(status_code=500, detail="Error creating voice")
    return voice


async def update_voice(voice_id: str, voice: Voice) -> Voice:
    try:
        voice_update = voice.model_dump(
            exclude_unset=True, exclude={"_id", "created_at", "updated_at"}
        )

        # update voice
        DB_COLLECTIONS["voices"].update_one({"_id": voice_id}, {"$set": voice_update})
        voice = await get_voice(voice_id=voice_id)
    except Exception as e:
        LOGGER.error(f"Error updating voice: {e}")
        raise HTTPException(status_code=500, detail="Error updating voice")
    return voice


async def delete_voice(voice_id: PydanticObjectId) -> Voice:
    try:
        # check if voice exists and fetch it
        voice = await get_voice(voice_id=voice_id)
        # delete voice
        DB_COLLECTIONS["voices"].delete_one({"_id": voice_id})
    except Exception as e:
        LOGGER.error(f"Error deleting voice: {e}")
        raise HTTPException(status_code=500, detail="Error deleting voice")
    return voice


async def validate_voice_mapping(voice: Voice, api_engine: API_Engine_Base) -> Voice:
    # check if voice belongs to the engine module in use
    if (
        voice.module != voice.module
        or voice.module != api_engine.ai_api_engine.__class__.__name__
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid engine module: {voice.module}",
        )

    # check if voice is actually listed by the current module
    voices: List[str] = await api_engine.ai_api_engine.get_voices()
    if voice.name not in voices and voice.module_voice_id not in voices:
        raise HTTPException(
            status_code=400,
            detail=f"Voice not found in module: {voice.name}",
        )

    # check if voice talent exists
    voice_talent = await get_voice_talent(voice_talent_id=voice.voice_talent_id)

    # update last_validated field
    voice.last_validated = datetime.now()
    DB_COLLECTIONS["voices"].update_one(
        {"_id": voice.id}, {"$set": {"last_validated": voice.last_validated}}
    )

    return voice


async def map_voice(voice_map: Voice_Map, api_engine: API_Engine_Base) -> Voice:
    # Check if voice exists and apply voice map
    voice: Voice = await get_voice(voice_id=voice.id)
    voice = Voice(**voice.model_dump(), **voice_map.model_dump())

    # Validate voice
    voice = await validate_voice_mapping(voice=voice, api_engine=api_engine)

    # Update voice
    voice = await update_voice(voice_id=voice.id, voice=voice_map)

    return voice

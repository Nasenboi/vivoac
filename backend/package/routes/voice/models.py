"""########################################################################################
Name: voice/models.py
Description: 
Imports:
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ...utils.models import CreatedUpdatedAt, CustomDateTime, PydanticObjectId
from ..engine_backend.models import AI_API_ENGINE_MODULE_KEYS
from .functions import *

"""
########################################################################################"""


class Voice(BaseModel, CreatedUpdatedAt):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    last_validated: Optional[CustomDateTime] = None
    voice_talent_id: Optional[PydanticObjectId] = None
    name: Optional[str] = None
    module: Optional[AI_API_ENGINE_MODULE_KEYS] = None
    module_voice_id: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[List[str]] = None


class Voice_Map(BaseModel):
    voice_id: PydanticObjectId
    voice_talent_id: PydanticObjectId
    module: AI_API_ENGINE_MODULE_KEYS
    module_voice_id: str


# -- Query Model --
# Ignore all fields that do not fit into a query
class Voice_Query(Voice):
    pass

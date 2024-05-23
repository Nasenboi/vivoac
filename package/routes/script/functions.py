"""########################################################################################
Name: script/functions.py
Description: 
Imports:
"""

from typing import List, Union

from fastapi import HTTPException

from ...globals import LOGGER, SETTINGS_GLOBAL
from ..session.models import Session
from .models import *

"""
########################################################################################"""


async def get_script_lines(
    script_line: Script_Line, session: Session = Session()
) -> Union[List[Union[Script_Line | dict]], Script_Line, dict]:
    LOGGER.debug(f"Getting script: {script_line}")
    return script_line

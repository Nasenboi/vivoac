"""########################################################################################
Name: script/functions.py
Description: 
Imports:
"""

from typing import List, Union

from fastapi import HTTPException

from ...globals import LOGGER, SETTINGS_GLOBAL
from .models import *

"""
########################################################################################"""


def get_script_lines(script: Script) -> Union[List[Union[Script]], Script]:
    LOGGER.debug(f"Getting script: {script}")

    if script.is_empty():
        LOGGER.warning(f"Recieved an empty script")
        raise HTTPException(status_code=400, detail="Recieved an empty script")

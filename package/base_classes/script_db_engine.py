"""########################################################################################
Name: script_db_engine.py
Description: 
Imports:
"""

from typing import Annotated, List, Union

from annotated_types import Ge, Le
from pydantic import confloat

from ..routes.script.models import Character_Info, Script
from ..utils.decorators import virtual

"""
########################################################################################"""


class Script_DB_Engine:
    # class variables:
    script_name: str = None

    def __init__(self, script_name: str = None):
        self.script_name = script_name

    ############################################################
    # getter functions:

    @virtual
    def get_script_names(self) -> List[str]:
        pass

    @virtual
    def get_script_lines(
        self, script: Script = Script()
    ) -> Union[List[Script], Script]:
        pass

    @virtual
    def get_character_infos(
        self, character_info: Character_Info = Character_Info()
    ) -> Union[List[Character_Info], Character_Info]:
        pass

    def get_class_variables(self):
        return self.__annotations__

    ############################################################
    # set class variables:

    def set_class_variables(self, *kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

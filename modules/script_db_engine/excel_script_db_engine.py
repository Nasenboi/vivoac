'''########################################################################################
Name: script_db_engine.py
Description: 
Imports:
'''
from ...package.base_classes.script_db_engine import Script_DB_Engine
from ...package.routes.script.models import Script, Character_Info
from typing import List, Union
import panads as pd
'''
########################################################################################'''

class Excel_Script_DB_Engine(Script_DB_Engine):
    # class variables:
    script_path: str = None
    script_file_name: str = None
    

    def __init__(self, script_path: str = None, script_file_name: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.script_path = script_path
        self.script_file_name = script_file_name


    ############################################################
    # getter functions:

    def get_script_names(self) -> List[str]:
        pass

    def get_script_lines(self, script: Script = Script()) -> Union[List[Script], Script]:
        pass

    def get_character_infos(self, character_info: Character_Info = Character_Info()) -> Union[List[Character_Info], Character_Info]:
        pass


    ############################################################
    # excel specific functions:

    def loaf_excel_script(self) -> :
        
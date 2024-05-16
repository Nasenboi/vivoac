"""########################################################################################
Name: excel_script_db_engine.py
Description: 
Imports:
"""

import os
from typing import List, Union

import pandas as pd

from ...package.base_classes.script_db_engine import Script_DB_Engine
from ...package.globals import LOGGER
from ...package.routes.script.models import Character_Info, Script

"""
########################################################################################"""


class Excel_Script_DB_Engine(Script_DB_Engine):
    # class variables:
    script_path: str = None
    script_file_name: str = None
    excel_data_frame: pd.DataFrame = None

    def __init__(
        self, script_path: str = None, script_file_name: str = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.script_path = script_path
        self.script_file_name = script_file_name

        try:
            self.load_excel_script()
        except Exception as e:
            LOGGER.info(f"Error loading excel script on initialization: {e}")

    ############################################################
    # getter functions:

    def get_script_names(self) -> List[str]:
        if not self.check_excel_script():
            return []

    def get_script_lines(
        self, script: Script = Script()
    ) -> Union[List[Script], Script]:
        if not self.check_excel_script():
            return Script()

    def get_character_infos(
        self, character_info: Character_Info = Character_Info()
    ) -> Union[List[Character_Info], Character_Info]:
        if not self.check_excel_script():
            return Character_Info()

    ############################################################
    # set class variables, expanding the base function to reload the excel script:

    def set_class_variables(self, *kwargs):
        super().set_class_variables(*kwargs)
        self.load_excel_script()

    ############################################################
    # excel specific functions:

    def load_excel_script(self) -> pd.DataFrame:
        # check if excel paths are given and the excel file exists:
        if self.script_path == None or self.script_file_name == None:
            raise ValueError("Excel file path or name not given!")

        if not os.path.exists(self.script_path + self.script_file_name):
            raise FileNotFoundError("Excel file does not exist!")

        self.excel_data_frame = pd.read_excel(self.script_path + self.script_file_name)

    def check_excel_script(self) -> bool:
        if self.excel_data_frame is not None:
            return True

        try:
            self.load_excel_script()
            return True
        except Exception as e:
            LOGGER.warning(f"Error loading excel script: {e}")
            return False

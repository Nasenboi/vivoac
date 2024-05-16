"""########################################################################################
Name: excel_script_db_engine.py
Description: 
Imports:
"""

import os
from typing import Annotated, Dict, List, Union

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
    field_name_mapping: Annotated[Dict[str, str], "'Script field': 'Excel field'"] = {
        "id": "id",
        "source_text": "source_text",
        "translation": "translation",
        "time_restriction": "time_restriction",
        "voice_talent": "voice_talent",
        "character_name": "character_name",
        "reference_audio_path": "reference_audio_path",
        "delivery_audio_path": "delivery_audio_path",
        "generatied_audio_path": "generatied_audio_path",
    }

    def __init__(
        self, script_path: str = None, script_file_name: str = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.script_path = script_path
        self.script_file_name = script_file_name

        try:
            self.__load_excel_script()
        except Exception as e:
            LOGGER.info(f"Error loading excel script on initialization: {e}")

    ############################################################
    # getter functions:

    def get_script_names(self) -> List[str]:
        if not self.__check_excel_script():
            return []

    def get_script_lines(
        self, script: Script = Script()
    ) -> Union[List[Script], Script]:
        # Checks before we search the database:
        if not self.__check_excel_script():
            return Script()
        if script.is_empty():
            LOGGER.warning("The given Script is empty!")
            return Script()

        # Get all fitting script lines from the database:
        filtered_database = self.__filter_database(script)

        # Return the results properly:
        if len(filtered_database) < 1:
            LOGGER.warning("No lines found in the database!")
            return Script()
        elif len(filtered_database) == 1:
            reverse_mapper = {v: k for k, v in self.field_name_mapping.items()}
            return Script(
                {
                    {
                        reverse_mapper[key]: value
                        for key, value in filtered_database.iloc[0].items()
                    }
                }
            )
        else:
            return [
                Script({{key: value for key, value in line.to_dict().items()}})
                for line in filtered_database
            ]

    def get_character_infos(
        self, character_info: Character_Info = Character_Info()
    ) -> Union[List[Character_Info], Character_Info]:
        if not self.__check_excel_script():
            return Character_Info()

    ############################################################
    # set class variables, expanding the base function to reload the excel script:

    def set_class_variables(self, *kwargs):
        super().set_class_variables(*kwargs)
        self.__load_excel_script()

    ############################################################
    # excel specific functions:
    def __check_excel_script(self) -> bool:
        if self.excel_data_frame is not None:
            return True

        try:
            self.__load_excel_script()
            return True
        except Exception as e:
            LOGGER.warning(f"Error loading excel script: {e}")
            return False

    def __load_excel_script(self) -> pd.DataFrame:
        # check if excel paths are given and the excel file exists:
        if self.script_path == None or self.script_file_name == None:
            raise ValueError("Excel file path or name not given!")

        if not os.path.exists(self.script_path + self.script_file_name):
            raise FileNotFoundError("Excel file does not exist!")

        self.excel_data_frame = pd.read_excel(self.script_path + self.script_file_name)

    def __filter_database(self, script: Script) -> pd.DataFrame:
        # filter the database with the given script parameters:
        query = pd.Series([True] * len(self.excel_data_frame))
        for key, value in script.model_dump():
            if value is not None:
                query &= self.excel_data_frame[self.field_name_mapping[key]] == value

        filtered_database = self.excel_data_frame[query]

        return filtered_database

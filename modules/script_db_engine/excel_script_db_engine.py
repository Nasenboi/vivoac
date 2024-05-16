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
        if not os.path.exists(self.script_path):
            LOGGER.warning("The given path does not exist!")
            return []

        scripts = [
            file for file in os.listdir(self.script_path) if file.endswith(".xlsx")
        ]

        if len(scripts) < 1:
            LOGGER.warning("No scripts found in the given path!")
            return []
        return scripts

    def get_script_lines(
        self, script: Script = Script()
    ) -> Union[List[Script], Script]:
        # Checks before we search the database:
        if not self.__check_excel_script():
            return Script()
        if script.is_empty():
            LOGGER.warning("The given Script is empty, returning all script lines!")

        # Get all fitting script lines from the database:
        filtered_database = self.__filter_database(script)

        # Return the results properly:
        if len(filtered_database) < 1:
            LOGGER.warning("No lines found in the database!")
            return Script()
        elif len(filtered_database) == 1:
            return Script(
                {{key: value for key, value in filtered_database.iloc[0].items()}}
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
        if character_info.is_empty():
            LOGGER.warning(
                "The given Character_Info is empty returning infos to all characters!"
            )

        character_names = self.__get_character_names(character_info)
        if character_info.character_name is not None or len(character_names) == 1:
            return self.__gather_character_info(character_info)

        character_info_list = []
        for name in character_names:
            character_info_list.append(
                self.__gather_character_info(Character_Info(character_name=name))
            )
        return character_info_list

    ############################################################
    # set class variables, expanding the base function to reload the excel script:

    def set_class_variables(self, *kwargs):
        super().set_class_variables(*kwargs)
        self.__load_excel_script()

    ############################################################
    # excel specific functions:
    def __load_excel_script(self) -> pd.DataFrame:
        # check if excel paths are given and the excel file exists:
        if self.script_path == None or self.script_file_name == None:
            raise ValueError("Excel file path or name not given!")

        if not os.path.exists(self.script_path + self.script_file_name):
            raise FileNotFoundError("Excel file does not exist!")

        self.excel_data_frame = pd.read_excel(self.script_path + self.script_file_name)
        self.__apply_field_mapping()

    def __apply_field_mapping(self):
        # apply the field mapping and additionally check if fields even exist:
        for script_field, excel_field in self.field_name_mapping.items():
            if excel_field not in self.excel_data_frame.columns:
                LOGGER.warning(f"Excel field '{excel_field}' does not exist!")
                self.field_name_mapping[script_field] = None

            self.excel_data_frame.rename(
                columns={excel_field: script_field}, inplace=True
            )

    def __check_excel_script(self) -> bool:
        if self.excel_data_frame is not None:
            return True

        try:
            self.__load_excel_script()
            return True
        except Exception as e:
            LOGGER.warning(f"Error loading excel script: {e}")
            return False

    def __filter_database(self, script: Script) -> pd.DataFrame:
        # filter the database with the given script parameters:
        query = pd.Series([True] * len(self.excel_data_frame))
        for key, value in script.model_dump():
            if value is not None:
                query &= self.excel_data_frame[key] == value

        filtered_database = self.excel_data_frame[query]
        return filtered_database

    def __get_character_names(self, character_info: Character_Info) -> List[str]:
        return (
            self.excel_data_frame[
                character_info.voice_talent == self.excel_data_frame["voice_talent"]
            ]["character_name"]
            .unique()
            .tolist()
        )

    def __gather_character_info(self, character_info: Character_Info) -> Character_Info:
        # gather all character info from the excel script
        # using search parameters from the given character_info object
        character_info.voice_talent = self.excel_data_frame[
            self.excel_data_frame["character_name"] == character_info.character_name
        ]["voice_talent"].unique()[0]
        character_info.script_name = (
            self.script_file_name.split(".")[0]
            if character_info.script_name is None
            else character_info.script_name
        )
        character_info.number_of_lines = (
            len(
                self.excel_data_frame[
                    self.excel_data_frame["character_name"]
                    == character_info.character_name
                ]
            )
            if character_info.number_of_lines is None
            else character_info.number_of_lines
        )
        character_info.gender = (
            self.excel_data_frame[
                self.excel_data_frame["character_name"] == character_info.character_name
            ]["gender"].unique()[0]
            if character_info.gender is None
            else character_info.gender
        )
        return character_info

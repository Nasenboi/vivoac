"""########################################################################################
Name: excel_script_db_engine.py
Description: This script db engine will be used for excel "databases"
it tries to convert the given excel database into a pandas dataframe and do all operations
using the given dataframe.
Imports:
"""

import os
from typing import Annotated, Dict, List, Union

import pandas as pd

from ...base_classes import Script_DB_Engine
from ...globals import LOGGER
from ...routes.script.models import Character_Info, Script_Line

"""
########################################################################################"""


class Excel_Script_DB_Engine(Script_DB_Engine):
    # class variables:
    script_path: str = None
    script_file_name: str = None
    excel_data_frame: pd.DataFrame = None
    field_name_mapping: Annotated[Dict[str, str], "'Script field': 'Excel field'"] = {
        "id": "rain_id",
        "source_text": "source_text",
        "translation": "translation",
        "time_restriction": "time_restriction",
        "voice_talent": "voice_talent",
        "character_name": "character_name",
        "reference_audio_path": "RA_path",
        "delivery_audio_path": "DA_path",
        "generatied_audio_path": "generatied_audio_path",
        "comment": "comment_1",
        "direction_notes": "direction_notes",
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

        try:
            if len(scripts) < 1:
                LOGGER.warning("No scripts found in the given path!")
                return []
        except Exception as e:
            LOGGER.error(f"Error getting script names: {e}")
            return []
        return scripts

    def get_script_lines(
        self, script: Script_Line = Script_Line()
    ) -> List[Script_Line]:
        # Checks before we search the database:
        filtered_database = []
        if not self.__check_excel_script():
            return []
        if script == None:
            LOGGER.warning("No Script_Line given, returning all script lines!")
            script = Script_Line()
            filtered_database = self.excel_data_frame
        elif script.is_empty():
            LOGGER.warning("The given Script is empty, returning all script lines!")
            filtered_database = self.excel_data_frame
        else:
            filtered_database = self.__filter_database(script)

        # Return the results properly:
        try:
            if len(filtered_database) < 1:
                LOGGER.warning("No lines found in the database!")
                return []
        except Exception as e:
            LOGGER.error(f"Error getting script lines: {e}")
            return []
        else:

            def script_line_model_dump(line):
                script_line = Script_Line()
                for key, value in line.items():
                    if key is not None and hasattr(script_line, key):
                        setattr(script_line, key, str(value))
                return script_line

            return [
                script_line_model_dump(line)
                for line in filtered_database.to_dict(orient="records")
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

    def get_class_variables(self):
        return {
            "script_path": self.script_path,
            "script_file_name": self.script_file_name,
            "field_name_mapping": self.field_name_mapping,
        }

    def set_class_variables(self, **kwargs):
        super().set_class_variables(**kwargs)
        LOGGER.debug(f"Reloading excel script:{self.script_file_name}")
        self.__load_excel_script()

    ############################################################
    # excel specific functions:
    def __load_excel_script(self) -> pd.DataFrame:
        # check if excel paths are given and the excel file exists:
        if self.script_path == None or self.script_file_name == None:
            LOGGER.error("No script path or file name given!")
            return
        if not os.path.exists(os.path.join(self.script_path, self.script_file_name)):
            LOGGER.error("Excel file does not exist!")
            return
        full_path = self.script_path + "/" + self.script_file_name
        self.excel_data_frame = pd.read_excel(full_path)
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
            if self.excel_data_frame is not None:
                return True
        except Exception as e:
            LOGGER.warning(f"Error loading excel script: {e}")
        return False

    def __filter_database(self, script: Script_Line) -> pd.DataFrame:
        # filter the database with the given script parameters:
        if not self.__check_excel_script():
            return pd.DataFrame()
        query = pd.Series([True] * len(self.excel_data_frame))
        parameters_to_filter = script.get_filter_params()
        for key, value in parameters_to_filter.items():
            query &= self.excel_data_frame[key].astype(str) == str(value)

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
        if not self.__check_excel_script():
            return Character_Info()
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

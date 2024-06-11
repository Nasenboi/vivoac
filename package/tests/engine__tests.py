"""########################################################################################
Name: tests/engine_test.py
Description: 
Imports:
"""

from ..globals import LOGGER
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class Engine_Tests(Test_Class):
    # class variables
    route: str = "engine"
    session_id: str = "test_session_id"

    def get_engines(self) -> test_function_return:
        LOGGER.debug(f"Starting the Engine Test: get_engines")
        response = self.client.get(
            url=f"/engine/get/",
            headers={"session-id": self.session_id},
        )
        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            message=str(response.json()),
            error_message=None,
        )
        LOGGER.debug(f"Results: {results}")
        return results

    def get_engine_settings(self) -> test_function_return:
        LOGGER.debug(f"Starting the Engine Test: get_engine_settings")
        engines_to_test = ["ai_api_engine", "audio_file_engine", "script_db_engine"]
        for engine in engines_to_test:
            response = self.client.get(
                url=f"/engine/settings/get",
                headers={"session-id": self.session_id},
                params={"engine_module_name": engine},
            )
            LOGGER.debug(f"Response: {response}")
            results = test_function_return(
                result="success" if response.status_code == 200 else "assert",
                http_code=response.status_code,
                message=str(response.json()),
                error_message=None,
            )
            LOGGER.debug(f"Results: {results}")

    test_functions = [get_engines, get_engine_settings]

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
            url=f"/engine/get/{self.session_id}",
        )
        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            message=str(response.json()),
            error_message=None,
        )
        LOGGER.debug(f"Results: {results}")
        return results

    test_functions = []

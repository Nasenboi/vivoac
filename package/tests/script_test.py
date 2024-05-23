"""########################################################################################
Name: tests/script_test.py
Description: This script tester class with test all functions inside the script route
Imports:
"""

from ..globals import LOGGER
from ..routes.script.models import Script_Line
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class Script_Test(Test_Class):
    # class variables
    route: str = "script"
    session_id: str = "test_session_id"

    def get_script(self) -> test_function_return:
        LOGGER.debug(f"Starting the Script Test: get_by_id")
        response = self.client.get_with_payload(
            url=f"/script/get/",
            headers={"session-id": self.session_id},
            json={
                "script_line": Script_Line(
                    character_name="test_character_name", id="0001"
                ).__dict__
            },
        )
        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            message=str(response.json()),
            error_message=None,
        )
        LOGGER.debug(f"Results: {results}")
        return results

    test_functions = [get_script]

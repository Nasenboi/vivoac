"""########################################################################################
Name: tests/script_test.py
Description: This script tester class with test all functions inside the script route
Imports:
"""

from ..globals import LOGGER
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class Script_Test(Test_Class):
    # class variables
    route: str = "script"
    session_id: str = "test_session_id"

    def get_by_id(self):
        LOGGER.debug(f"Starting the Script Test: get_by_id")
        response = self.client.get(
            url=f"/session/get/{self.session_id}",
        )

    test_functions = [get_by_id]

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
    session_id: str = "test_session_id"

    def create_with_id(self):
        LOGGER.debug(f"Starting the Script Test: get_by_id")
        response = self.client.put(
            url=f"/session/create",
            json={"session_id": self.session_id},
        )
        assert response.status_code == 200
        assert response.json() == {"session_id": self.session_id}

    test_functions = [create_with_id]

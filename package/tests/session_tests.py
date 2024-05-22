"""########################################################################################
Name: tests/script_test.py
Description: This script tester class with test all functions inside the script route
Imports:
"""

from ..globals import LOGGER
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class Session_Test(Test_Class):
    # class variables
    route: str = "session"

    def create_with_id(self):
        LOGGER.debug(f"Starting the Script Test: create_with_id")
        response = self.client.put(
            url=f"/session/create",
            json={"session_id": self.session_id},
        )
        assert response.status_code == 200
        assert response.json() == {"session_id": self.session_id}
        test_function_return(
            result="success",
            http_code=response.status_code,
            message=f"Session created with id: {self.session_id}",
            error_message=None,
        )

    test_functions = [create_with_id]

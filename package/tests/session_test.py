"""########################################################################################
Name: tests/script_test.py
Description: This script tester class with test all functions inside the script route
Imports:
"""

from fastapi.testclient import TestClient

from ..globals import LOGGER
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class Session_Test(Test_Class):
    # class variables
    route: str = "session"
    session_id: str = "test_session_id"

    def create_with_id(self) -> test_function_return:
        LOGGER.debug(f"create_with_id")
        response = self.client.put(
            url=f"/session/create",
            json={"session_id": self.session_id},
        )
        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            message=str(response.json()),
            error_message=None,
        )
        LOGGER.debug(f"Results: {results}")
        return results

    def get_with_id(self) -> test_function_return:
        LOGGER.debug(f"get_with_id")
        response = self.client.get(
            url=f"/session/get/{self.session_id}",
        )
        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            message=str(response.json()),
            error_message=None,
        )
        LOGGER.debug(f"Results: {results}")
        return results

    def delete_with_id(self) -> test_function_return:
        LOGGER.debug(f"delete_with_id")
        response = self.client.post(
            url=f"/session/close",
            json={"session_id": self.session_id},
        )
        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            message=str(response.json()),
            error_message=None,
        )
        LOGGER.debug(f"Results: {results}")
        return results

    test_functions = [create_with_id, get_with_id, delete_with_id]

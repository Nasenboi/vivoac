"""########################################################################################
Name: tests/script_test.py
Description: This script tester class with test all functions inside the script route
Imports:
"""

from ..globals import LOGGER
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class Session_Tests(Test_Class):
    # class variables
    route: str = "session"
    session_id: str = "test_session_id"
    setting_updates = {
        "session_settings": {
            "audio_format": {
                "sample_rate": 44100,
                "bit_depth": 24,
            }
        }
    }

    def create_session(self) -> test_function_return:
        LOGGER.debug(f"create_session")
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

    def get_session(self) -> test_function_return:
        LOGGER.debug(f"get_session")
        response = self.client.get(
            url=f"/session/get/",
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

    def update_session(self) -> test_function_return:
        LOGGER.debug(f"update_session")
        response = self.client.post(
            url=f"/session/update",
            headers={"session-id": self.session_id},
            json={**self.setting_updates},
        )
        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            message=str(response.json()),
            error_message=None,
        )
        LOGGER.debug(f"Results: {results}")
        return results

    def delete_session(self) -> test_function_return:
        LOGGER.debug(f"delete_session")
        response = self.client.post(
            url=f"/session/close",
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

    def create_test_session(self):
        self.create_session()

    test_functions = [
        create_session,
        get_session,
        update_session,
        delete_session,
        create_test_session,
    ]

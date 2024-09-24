"""########################################################################################
Name: tests/test_class.py
Description: This class is used to build unified tests for each route of the API
Imports:
"""

from time import time
from typing import List, Literal, Optional, Type

from fastapi.responses import Response
from package.utils.classes.test_client import CustomTestClient
from pydantic import BaseModel

from ..globals import LOGGER

"""
########################################################################################"""


class test_function_return(BaseModel):
    function: Optional[str] = ""
    test_class: Optional[str] = ""
    result: Literal["success", "failed"] = "success"
    http_code: Optional[int] = None
    message: Optional[str] = None
    error_message: Optional[str] = None
    time: Optional[str] = None
    should_fail: Optional[bool] = False


class Test_Class:
    # class variables
    route: str = None
    client: Type[CustomTestClient] = None
    test_user: dict = None
    token: str = None
    test_functions: List[callable] = []
    api_version: str = None
    base_header: dict = None

    def __init__(self, client, test_user, token, api_version):
        self.client = client
        self.test_user = test_user
        self.token = token
        self.api_version = api_version

        self.base_header = {
            "Authorization": f"Bearer {self.token}",
            "api-version": self.api_version,
        }

    def test_script(self) -> list[dict]:
        LOGGER.info(f"Starting the Script Tests for route: {self.route}")
        results = []
        for function in self.test_functions:
            start_time = time()
            result = function(self)
            result.time = str(time() - start_time)
            result.function = function.__name__
            result.test_class = self.__class__.__name__
            results.append(result.model_dump())

        LOGGER.info(f"Finished the Script Tests for route: {self.route}")
        return results

    def generate_test_result(
        self, response: Response, should_fail=False
    ) -> test_function_return:
        test_sucessful: bool = (
            response.status_code != 200 if should_fail else response.status_code == 200
        )
        message_type = {}
        message_content = str(response.json().get("data"))
        if test_sucessful:
            message_type["message"] = message_content
        else:
            message_type["error_message"] = message_content
        return test_function_return(
            result="success" if test_sucessful else "failed",
            http_code=response.status_code,
            should_fail=should_fail,
            **message_type,
        )

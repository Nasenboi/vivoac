"""########################################################################################
Name: tests/test_class.py
Description: This class is used to build unified tests for each route of the API
Imports:
"""

from time import time
from typing import List, Literal, Optional, Type

from package.utils.classes.test_client import CustomTestClient
from pydantic import BaseModel

from ..globals import LOGGER

"""
########################################################################################"""


class test_function_return(BaseModel):
    function: Optional[str] = ""
    test_class: Optional[str] = ""
    result: Literal["success", "assert"] = "success"
    http_code: Optional[int] = None
    message: Optional[str] = "This is an empty function return message"
    error_message: Optional[str] = None
    time: Optional[str] = None


class Test_Class:
    # class variables
    route: str = None
    client: Type[CustomTestClient] = None
    test_user: dict = None
    token: str = None
    test_functions: List[callable] = []
    results: List[dict] = []
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

        for function in self.test_functions:
            start_time = time()
            result = function(self)
            result.time = str(time() - start_time)
            result.function = function.__name__
            result.test_class = self.__class__.__name__
            self.results.append(result.model_dump())

        LOGGER.info(f"Finished the Script Tests for route: {self.route}")
        return self.results

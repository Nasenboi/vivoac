"""########################################################################################
Name: tests/test_class.py
Description: This class is used to build unified tests for each route of the API
Imports:
"""

from typing import List, Literal, Optional

from pydantic import BaseModel

from ..globals import LOGGER
from ..utils.decorators import virtual

"""
########################################################################################"""


class test_function_return(BaseModel):
    result: Literal["success", "assert"] = "success"
    http_code: Optional[int] = None
    message: Optional[str] = "This is an empty function return message"
    error_message: Optional[str] = None


class Test_Class:
    # class variables
    route: str = None
    client = None
    test_functions: List = []
    results: List[test_function_return] = []

    def __init__(self, client):
        self.client = client

    def test_script(self):
        LOGGER.debug(f"Starting the Script Tests for route: {self.route}")

        for function in self.test_functions:
            self.results.append(function(self.client))

        LOGGER.debug(f"Finished the Script Tests for route: {self.route}")

        # Get the count of successfull and assert results
        success_count = sum(1 for result in self.results if result.result == "success")
        assertion_count = sum(1 for result in self.results if result.result == "assert")
        LOGGER.info(
            f"Results: {success_count} successfully, {assertion_count} assertions"
        )

'''########################################################################################
Name: tests/test_class.py
Description: This class is used to build unified tests for each route of the API
Imports:
'''
from ..package.utils.decorators import virtual 
from ..package.globals import LOGGER
from typing import Literal, Optional, List
from pydantic import BaseModel
'''
########################################################################################'''

class test_function_return(BaseModel):
    result: Literal["success", "assert"]
    http_code: int
    message: Optional[str]
    error_message: Optional[str]


class Test_Class():
    # class variables
    client = None
    test_functions: List[function] = []
    results: List[test_function_return]= []

    def __init__(self, client):
        self.client = client

    def test_script(self):
        LOGGER.debug(f"Starting the Script Tests for route: {self.__name__}")

        for function in self.test_functions:
            self.results.append(function(self.client))

        LOGGER.debug(f"Finished the Script Tests for route: {self.__name__}")

        # Get the count of successfull and assert results
        success_count = sum(1 for result in self.results if result.result == "success")
        assertion_count = sum(1 for result in self.results if result.result == "assert")
        LOGGER.info(f"Results: {success_count} successfully, {assertion_count} assertions")

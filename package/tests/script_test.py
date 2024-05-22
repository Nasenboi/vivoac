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

    def get_by_id(self) -> test_function_return:
        LOGGER.debug(f"Starting the Script Test: get_by_id")
        return test_function_return()

    test_functions = [get_by_id]

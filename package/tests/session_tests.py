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

    def get_by_id(self, client):
        LOGGER.debug(f"Starting the Script Test: get_by_id")

    test_functions = [get_by_id]

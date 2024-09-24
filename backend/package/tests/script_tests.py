"""########################################################################################
Name: tests/script_test.py
Description: This script tester class with test all functions inside the script route
Imports:
"""

from ..globals import LOGGER
from ..routes.script.models import Script_Line
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class Script_Tests(Test_Class):
    # class variables
    route: str = "script"

    def get_all_script_lines(self) -> test_function_return:
        response = self.client.get(
            url=f"/script/find",
            headers={**self.base_header},
        )
        return self.generate_test_result(response)

    test_functions = [get_all_script_lines]

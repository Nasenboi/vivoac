"""########################################################################################
Name: tests/engine_test.py
Description: 
Imports:
"""

from ..globals import LOGGER
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class Engine_Tests(Test_Class):
    # class variables
    route: str = "engine"
    session_id: str = "test_session_id"

    test_functions = []

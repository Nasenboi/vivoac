"""########################################################################################
Name: tests/engine_test.py
Description: 
Imports:
"""

from typing import get_args

from fastapi.responses import Response

from ..routes.engine_backend.models import ENGINE_TYPES
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class Engine_Tests(Test_Class):
    # class variables
    route: str = "engine"

    def get_engine_names(self) -> test_function_return:
        response = self.client.get(
            url=f"/engine/names",
            headers={**self.base_header},
        )
        return self.generate_test_result(response)

    def get_engine_modules(self, engine_type: ENGINE_TYPES) -> Response:
        return self.client.get(
            url=f"/engine/get_modules/" + engine_type,
            headers={**self.base_header},
        )

    def get_both_module_lists(self) -> test_function_return:
        modules = {}
        for engine in get_args(ENGINE_TYPES):
            response = self.get_engine_modules(engine)
            if response.status_code != 200:
                return self.generate_test_result(response)
            else:
                modules[engine] = response.json().get("data")

        return self.generate_test_result(response, alt_message=modules)

    def get_engine_settings(self, engine_type: ENGINE_TYPES) -> Response:
        return self.client.get(
            url=f"/engine/settings/{engine_type}/get",
            headers={**self.base_header},
        )

    def get_both_engine_settings(self) -> test_function_return:
        settings = {}
        for engine in get_args(ENGINE_TYPES):
            response = self.get_engine_settings(engine)
            if response.status_code != 200:
                return self.generate_test_result(response)
            else:
                settings[engine] = response.json().get("data")

        return self.generate_test_result(response, alt_message=settings)

    test_functions = [get_engine_names, get_both_module_lists, get_both_engine_settings]

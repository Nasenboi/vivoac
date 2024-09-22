from typing import Type

from test_class import Test_Class

__all__ = ["get_test_classes"]


def get_test_classes() -> list[Type[Test_Class]]:
    from .ai_api_test import AI_API_Tests
    from .engine_tests import Engine_Tests
    from .script_tests import Script_Tests

    return [Script_Tests, Engine_Tests, AI_API_Tests]

from typing import List, Type

from .test_class import Test_Class

__all__ = ["get_test_classes"]


def get_test_classes() -> List[Type[Test_Class]]:
    from .ai_api_test import AI_API_Tests
    from .engine_tests import Engine_Tests
    from .script_tests import Script_Tests
    from .user_tests import User_Tests
    from .voice_talent_tests import Voice_Talent_Tests

    return [Script_Tests, Engine_Tests, AI_API_Tests, Voice_Talent_Tests, User_Tests]

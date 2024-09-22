"""########################################################################################
Name: tests/voice_talent_tests.py
Description: This voice_talent tester class with test all functions inside the voice_talent route
Imports:
"""

from ..globals import LOGGER
from ..routes.script.models import Script_Line
from ..routes.voice_talent.models import Voice_Talent
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class Voice_Talent_Tests(Test_Class):
    # class variables
    route: str = "voice_talent"

    test_voice_talent: Voice_Talent = Voice_Talent(
        first_name="Max",
        last_name="Mustermann",
        email="max.mustermann@vivoac.de",
        birth_date="today",
        gender="male",
    )

    def create_voice_talent(self) -> test_function_return:
        LOGGER.debug(f"Starting the Voice Talent Test: ")
        response = self.client.post(
            url=f"/voice_talent/",
            headers={**self.base_header},
            json=self.test_voice_talent.model_dump(
                exclude_unset=True, exclude={"id", "created_at", "updated_at"}
            ),
        )
        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            message=str(response.json().get("data")),
            error_message=None,
        )
        return results

    test_functions = [create_voice_talent]

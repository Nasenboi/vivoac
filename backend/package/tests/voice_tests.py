"""########################################################################################
Name: tests/voice_tests.py
Description: This voice tester class with test all functions inside the voice route
Imports:
"""

from datetime import datetime

from fastapi.responses import Response
from package.globals import LOGGER

from ..routes.voice.models import Voice
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class Voice_Tests(Test_Class):
    # class variables
    route: str = "voice"

    test_voice: Voice = Voice(
        name="max_voice_01",
        description="This is the first voice for max",
        labels=["max", "voice"],
    )

    def create_voice(self) -> test_function_return:
        response = self.client.post(
            url=f"/voice/crud",
            headers={**self.base_header},
            json=self.test_voice.model_dump(
                exclude_unset=True,
                exclude={"id", "created_at", "updated_at"},
            ),
        )
        self.test_voice.id = response.json().get("data").get("_id")
        if not self.test_voice.id:
            LOGGER.warning(
                "No ID returned from the response, something is seriously wrong!"
            )
            return self.generate_test_result(
                alt_code=404, alt_message={"No ID returned"}
            )
        return self.generate_test_result(response)

    def dont_create_duplicate(self) -> test_function_return:
        response = self.client.post(
            url=f"/voice/crud",
            headers={**self.base_header},
            json=self.test_voice.model_dump(
                exclude_unset=True, exclude={"id", "created_at", "updated_at"}
            ),
        )
        return self.generate_test_result(response, should_fail=True)

    def get_voice_by_id(self) -> test_function_return:
        response = self.client.get(
            url=f"/voice/crud/{self.test_voice.id}",
            headers={**self.base_header},
        )
        return self.generate_test_result(response)

    def get_voice_by_query(self) -> test_function_return:
        response = self.client.get(
            url=f"/voice/find",
            headers={**self.base_header},
            params={
                "name": self.test_voice.name,
            },
        )
        return self.generate_test_result(response)

    def update_voice(self) -> test_function_return:
        response = self.client.put(
            url=f"/voice/crud/{self.test_voice.id}",
            headers={**self.base_header},
            json={
                "description": "A way better description",
            },
        )
        return self.generate_test_result(response)

    def delete_voice(self) -> test_function_return:
        response = self.client.delete(
            url=f"/voice/crud/{self.test_voice.id}",
            headers={**self.base_header},
        )
        return self.generate_test_result(response)

    def voice_should_not_exist(self) -> test_function_return:
        response = self.client.get(
            url=f"/voice/crud/{self.test_voice.id}",
            headers={**self.base_header},
        )
        return self.generate_test_result(response, should_fail=True)

    test_functions = [
        create_voice,
        dont_create_duplicate,
        get_voice_by_id,
        get_voice_by_query,
        update_voice,
        delete_voice,
        voice_should_not_exist,
    ]

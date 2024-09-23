"""########################################################################################
Name: tests/voice_talent_tests.py
Description: This voice_talent tester class with test all functions inside the voice_talent route
Imports:
"""

from datetime import date

from fastapi.responses import Response
from package.globals import LOGGER

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
        birth_date=date.today().isoformat(),
        gender="male",
    )

    def create_voice_talent(self) -> test_function_return:
        response = self.client.post(
            url=f"/voice_talent/",
            headers={**self.base_header},
            json=self.test_voice_talent.model_dump(
                exclude_unset=True,
                exclude={"id", "created_at", "updated_at"},
            ),
        )
        self.test_voice_talent.id = response.json().get("data").get("_id")
        if not self.test_voice_talent.id:
            LOGGER.warning(
                "No ID returned from the response, something is seriously wrong!"
            )
            response = Response(status_code=404, content={"data": {"No ID returned"}})
        return self.generate_test_result(response)

    def dont_create_duplicate(self) -> test_function_return:
        response = self.client.post(
            url=f"/voice_talent/",
            headers={**self.base_header},
            json=self.test_voice_talent.model_dump(
                exclude_unset=True, exclude={"id", "created_at", "updated_at"}
            ),
        )
        return self.generate_test_result(response, should_fail=True)

    def get_voice_talent_by_id(self) -> test_function_return:
        response = self.client.get(
            url=f"/voice_talent/{self.test_voice_talent.id}",
            headers={**self.base_header},
        )
        return self.generate_test_result(response)

    def get_voice_talent_by_query(self) -> test_function_return:
        response = self.client.get(
            url=f"/voice_talent/",
            headers={**self.base_header},
            params={
                "first_name": self.test_voice_talent.first_name,
                "last_name": self.test_voice_talent.last_name,
                "email": self.test_voice_talent.email,
            },
        )
        return self.generate_test_result(response)

    def update_voice_talent(self) -> test_function_return:
        response = self.client.put(
            url=f"/voice_talent/{self.test_voice_talent.id}",
            headers={**self.base_header},
            json={
                "first_name": "Moritz",
            },
        )
        return self.generate_test_result(response)

    def delete_voice_talent(self) -> test_function_return:
        response = self.client.delete(
            url=f"/voice_talent/{self.test_voice_talent.id}",
            headers={**self.base_header},
        )
        return self.generate_test_result(response)

    def voice_talent_should_not_exist(self) -> test_function_return:
        response = self.client.get(
            url=f"/voice_talent/{self.test_voice_talent.id}",
            headers={**self.base_header},
        )
        return self.generate_test_result(response, should_fail=True)

    test_functions = [
        create_voice_talent,
        dont_create_duplicate,
        get_voice_talent_by_id,
        get_voice_talent_by_query,
        update_voice_talent,
        delete_voice_talent,
        voice_talent_should_not_exist,
    ]

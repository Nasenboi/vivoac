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
        response = self.client.post(
            url=f"/voice_talent/",
            headers={**self.base_header},
            json=self.test_voice_talent.model_dump(
                exclude_unset=True, exclude={"id", "created_at", "updated_at"}
            ),
        )
        message_type = {}
        message_content = str(response.json().get("data"))
        if response.status_code == 200:
            message_type["message"] = message_content
        else:
            message_type["error_message"] = message_content
        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            **message_type,
        )
        self.test_voice_talent.id = response.json().get("data").get("_id")
        return results

    def dont_create_duplicate(self) -> test_function_return:
        response = self.client.post(
            url=f"/voice_talent/",
            headers={**self.base_header},
            json=self.test_voice_talent.model_dump(
                exclude_unset=True, exclude={"id", "created_at", "updated_at"}
            ),
        )
        message_type = {}
        message_content = str(response.json().get("data"))
        if response.status_code != 200:
            message_type["message"] = message_content
        else:
            message_type["error_message"] = message_content
        results = test_function_return(
            result="success" if response.status_code != 200 else "assert",
            http_code=response.status_code,
            **message_type,
        )
        return results

    def get_voice_talent_by_id(self) -> test_function_return:
        response = self.client.get(
            url=f"/voice_talent/{self.test_voice_talent.id}",
            headers={**self.base_header},
        )
        message_type = {}
        message_content = str(response.json().get("data"))
        if response.status_code == 200:
            message_type["message"] = message_content
        else:
            message_type["error_message"] = message_content
        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            **message_type,
        )
        return results

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
        message_type = {}
        message_content = str(response.json().get("data"))
        if response.status_code == 200:
            message_type["message"] = message_content
        else:
            message_type["error_message"] = message_content
        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            **message_type,
        )
        return results

    def update_voice_talent(self) -> test_function_return:
        response = self.client.put(
            url=f"/voice_talent/{self.test_voice_talent.id}",
            headers={**self.base_header},
            json={
                "first_name": "Moritz",
            },
        )
        message_type = {}
        message_content = str(response.json().get("data"))
        if response.status_code == 200:
            message_type["message"] = message_content
        else:
            message_type["error_message"] = message_content
        results = test_function_return(
            result="success" if response.status_code != 200 else "assert",
            http_code=response.status_code,
            **message_type,
        )
        return results

    def delete_voice_talent(self) -> test_function_return:
        response = self.client.delete(
            url=f"/voice_talent/{self.test_voice_talent.id}",
            headers={**self.base_header},
        )
        message_type = {}
        message_content = str(response.json().get("data"))
        if response.status_code == 200:
            message_type["message"] = message_content
        else:
            message_type["error_message"] = message_content
        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            **message_type,
        )
        return results

    def voice_talent_should_not_exist(self) -> test_function_return:
        response = self.client.get(
            url=f"/voice_talent/{self.test_voice_talent.id}",
            headers={**self.base_header},
        )
        message_type = {}
        message_content = str(response.json().get("data"))
        if response.status_code != 200:
            message_type["message"] = message_content
        else:
            message_type["error_message"] = message_content
        results = test_function_return(
            result="success" if response.status_code != 200 else "assert",
            http_code=response.status_code,
            **message_type,
        )
        return results

    test_functions = [
        create_voice_talent,
        dont_create_duplicate,
        get_voice_talent_by_id,
        get_voice_talent_by_query,
        update_voice_talent,
        delete_voice_talent,
        voice_talent_should_not_exist,
    ]

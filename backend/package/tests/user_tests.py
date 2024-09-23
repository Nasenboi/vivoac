"""########################################################################################
Name: tests/user_tests.py
Description: This user tester class with test all functions inside the user route
Imports:
"""

from datetime import datetime

from fastapi.responses import Response
from package.globals import LOGGER

from ..routes.user.models import User, UserForEdit
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class User_Tests(Test_Class):
    # class variables
    route: str = "user"

    user_dummy: UserForEdit = UserForEdit(
        username="max_mustermann",
        first_name="Max",
        last_name="Mustermann",
        email="max.musermann@vivoac.de",
        role="user",
        disabled=False,
        password="ma10mus!erm4ann",
    )

    user_token: str = None

    def create_user(self) -> test_function_return:
        response = self.client.post(
            url=f"/user/",
            headers={**self.base_header},
            json=self.user_dummy.model_dump(
                exclude_unset=True,
                exclude={"id", "created_at", "updated_at"},
            ),
        )
        self.user_dummy.id = response.json().get("data").get("_id")
        if not self.user_dummy.id:
            LOGGER.warning(
                "No ID returned from the response, something is seriously wrong!"
            )
            response = Response(status_code=404, content={"data": {"No ID returned"}})
        return self.generate_test_result(response)

    test_functions = [create_user]

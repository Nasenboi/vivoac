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

    user_dummy_token: str = None

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
            LOGGER.warning("No ID returned from the response, something is wrong!")
            response = Response(status_code=404, content={"data": {"No ID returned"}})
        return self.generate_test_result(response)

    def get_user_by_id(self) -> test_function_return:
        response = self.client.get(
            url=f"/user/{self.user_dummy.id}",
            headers={**self.base_header},
        )
        return self.generate_test_result(response)

    def get_user_by_query(self) -> test_function_return:
        response = self.client.get(
            url=f"/user/",
            headers={**self.base_header},
            params={
                "first_name": self.user_dummy.first_name,
                "last_name": self.user_dummy.last_name,
                "email": self.user_dummy.email,
            },
        )
        return self.generate_test_result(response)

    def update_user(self) -> test_function_return:
        response = self.client.put(
            url=f"/user/{self.user_dummy.id}",
            headers={**self.base_header},
            json={
                "first_name": "Moritz",
            },
        )
        return self.generate_test_result(response)

    def login_as_user(self) -> test_function_return:
        auth = {
            "username": self.user_dummy.username,
            "password": self.user_dummy.password,
        }
        response = self.client.post("/token", data=auth)
        self.user_dummy_token = response.json().get("access_token")
        return self.generate_test_result(response)

    def check_if_token_works(self) -> test_function_return:
        response = self.client.get(
            "/user/whoami/",
            headers={
                "Authorization": f"Bearer {self.user_dummy_token}",
                "api-version": self.api_version,
            },
        )
        return self.generate_test_result(response)

    def invalid_tokens_should_fail(self) -> test_function_return:
        response = self.client.get(
            "/user/whoami/",
            headers={
                "Authorization": f"Bearer invalid_dummy_token",
                "api_version": self.api_version,
            },
        )
        return self.generate_test_result(response, should_fail=True)

    def delete_user(self) -> test_function_return:
        response = self.client.delete(
            url=f"/user/{self.user_dummy.id}",
            headers={**self.base_header},
        )
        return self.generate_test_result(response)

    def user_should_not_exist(self) -> test_function_return:
        response = self.client.get(
            url=f"/user/{self.user_dummy.id}",
            headers={**self.base_header},
        )
        return self.generate_test_result(response, should_fail=True)

    test_functions = [
        create_user,
        get_user_by_id,
        get_user_by_query,
        update_user,
        login_as_user,
        check_if_token_works,
        invalid_tokens_should_fail,
        delete_user,
        user_should_not_exist,
    ]

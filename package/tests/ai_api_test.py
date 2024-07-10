"""########################################################################################
Name: tests/ai_api_test.py
Description: 
Imports:
"""

import sys

from ..globals import LOGGER
from .test_class import Test_Class, test_function_return

"""
########################################################################################"""


class AI_API_Tests(Test_Class):
    # class variables
    route: str = "ai_api_handler"
    session_id: str = "test_session_id"

    def text_to_speech(self) -> test_function_return:
        LOGGER.debug(f"Starting the AI API Test: text_to_speech")
        if sys.platform != "linux":
            return test_function_return(
                result="assert",
                http_code=500,
                message="This test is only supported on Linux.",
                error_message=None,
            )

        response = self.client.post(
            url=f"/ai_api_handler/text_to_speech/",
            headers={"session-id": self.session_id, "api-key": "none"},
            json={
                "data": {
                    "text": "Brautkleid bleibt Brautkleid und Blaukraut bleibt Blaukraut. Bierbrauer Bauer braut braunes Bier, braunes Bier braut Bierbrauer Bauer.",
                    "voice": "de_DE-markus_haase-ep=2665",
                    "voice_settings": {},
                    "model": "none",
                    "seed": -1,
                }
            },
        )
        # Check if the response is successful
        try:
            if response.status_code == 200:
                # Save the file locally
                file_name = "./piper-voice/output.wav"
                with open(file_name, "wb") as file:
                    file.write(response.content)
                message = f"File saved successfully as {file_name}."
            else:
                message = "Failed to get a valid response."
        except Exception as e:
            message += f"Failed to save the file. Error: {str(e)}"

        results = test_function_return(
            result="success" if response.status_code == 200 else "assert",
            http_code=response.status_code,
            message=message,
            error_message=None,
        )
        return results

    test_functions = [text_to_speech]

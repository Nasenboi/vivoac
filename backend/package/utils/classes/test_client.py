"""########################################################################################
Name: utils/test_client.py
Description:
https://medium.com/@mehmetcanfarsak/solution-for-testclient-delete-payload-support-8ae12e153a3a
Imports:
"""

from fastapi.testclient import TestClient

"""
########################################################################################"""


class CustomTestClient(TestClient):
    def get_with_payload(self, **kwargs):
        return self.request(method="GET", **kwargs)

    def delete_with_payload(self, **kwargs):
        return self.request(method="DELETE", **kwargs)

# Basic Packages
import os
from dotenv import load_dotenv
import json
import unittest

# Local Packages
import black_scholes
import lennard_jones

# App Packages
import requests
from requests.auth import HTTPBasicAuth


class TestJetCert(unittest.TestCase):

    def setUp(self):
        host = os.getenv("HOST")
        port = os.getenv("PORT")
        self.base_url = f"http://{host}:{port}"

    def test_1_signup(self):
        url = self.base_url + "/signup"

        data = {
            "name": "Arman",
            "email": "armanheids@gmail.com",
            "password": "arman@JC",
        }

        response = requests.post(url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.text, "Successfully registered.")

    def test_2_black_scholes(self):
        url = self.base_url + "/black-scholes"

        test = next(black_scholes.input_generator())
        input_args = test.get("input_args")

        data = {
            "stockPrice": json.dumps(input_args[0].tolist()),
            "optionStrike": json.dumps(input_args[1].tolist()),
            "optionYears": json.dumps(input_args[2].tolist()),
            "Riskfree": json.dumps(input_args[3]),
            "Volatility": json.dumps(input_args[4]),
        }

        response = requests.get(
            url,
            auth=HTTPBasicAuth("armanheids@gmail.com", "arman@JC"),
            data=data,
        )

        self.assertEqual(response.status_code, 200)

    def test_3_lennard_jones(self):
        url = self.base_url + "/lennard-jones"

        test = next(lennard_jones.input_generator())
        input_args = test.get("input_args")

        data = {
            "cluster": json.dumps(input_args[0].tolist()),
        }

        response = requests.get(
            url,
            auth=HTTPBasicAuth("armanheids@gmail.com", "arman@JC"),
            data=data,
        )

        self.assertEqual(response.status_code, 200)

    def test_4_get_all_users(self):
        url = self.base_url + "/users"

        headers = {
            "admin-secret": os.getenv("ADMIN_SECRET"),
        }

        response = requests.get(url, headers=headers)

        users = json.loads(response.text)

        self.assertEqual(response.status_code, 200)

    def test_5_delete_user(self):
        url = self.base_url + "/users/armanheids@gmail.com"

        headers = {
            "admin-secret": os.getenv("ADMIN_SECRET"),
        }

        response = requests.delete(url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "User deleted successfully")


if __name__ == "__main__":
    load_dotenv()
    unittest.main()

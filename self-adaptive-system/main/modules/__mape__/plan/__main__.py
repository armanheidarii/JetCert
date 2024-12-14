import math
import json


def get_json_inputs():
    return json.loads(input())


def login_plan(login_analyse_data):
    if "version1" in login_analyse_data:
        return "version1"

    return "version2"


def crypto_plan(crypto_analyse_data):
    if "version1" in crypto_analyse_data:
        return "version1"

    if "version2" in crypto_analyse_data:
        return "version2"

    if "version3" in crypto_analyse_data:
        return "version3"

    return "version4"


def finance_plan(finance_analyse_data):
    if "version2" in finance_analyse_data:
        return "version2"

    return "version1"


def physics_plan(physics_analyse_data):
    if "version4" in physics_analyse_data:
        return "version4"

    if "version3" in physics_analyse_data:
        return "version3"

    if "version2" in physics_analyse_data:
        return "version2"

    return "version1"


analyse_data = get_json_inputs()

login_analyse_data = analyse_data.get("login")
crypto_analyse_data = analyse_data.get("cryptography")
finance_analyse_data = analyse_data.get("finance")
physics_analyse_data = analyse_data.get("physics")

plan_data = json.dumps(
    {
        "login": login_plan(login_analyse_data),
        "cryptography": crypto_plan(crypto_analyse_data),
        "finance": finance_plan(finance_analyse_data),
        "physics": physics_plan(physics_analyse_data),
    }
)

print(plan_data)

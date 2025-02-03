import math
import json


def get_json_inputs():
    return json.loads(input())


def login_plan(login_analyse_data):
    if "basic_auth" in login_analyse_data:
        return "basic_auth"

    return "safe_basic_auth"


def crypto_plan(crypto_analyse_data):
    if "wire" in crypto_analyse_data:
        return "wire"

    if "shift_cipher" in crypto_analyse_data:
        return "shift_cipher"

    if "triple_des" in crypto_analyse_data:
        return "triple_des"

    return "rsa"


def finance_plan(finance_analyse_data):
    if "numba_optimized" in finance_analyse_data:
        return "numba_optimized"

    return "numpy_optimized"


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

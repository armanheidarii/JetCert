import math
import json


def get_json_inputs():
    return json.loads(input())


def higher_level_planning(module_analyse_data):
    module_plan_fast_level = -1
    module_plan_safe_level = -1
    for plan in module_analyse_data:
        plan_state = plan.get("state")
        plan_level = plan.get("level")

        if plan_state == "fast" and plan_level > module_plan_fast_level:
            module_plan_fast_level = plan_level

        elif plan_state == "safe" and plan_level > module_plan_safe_level:
            module_plan_safe_level = plan_level

    if module_plan_fast_level > -1:
        return {"state": "fast", "level": module_plan_fast_level}

    if module_plan_safe_level > -1:
        return {"state": "safe", "level": module_plan_safe_level}


def lower_level_planning(module_analyse_data):
    module_plan_fast_level = math.inf
    module_plan_safe_level = math.inf
    for plan in module_analyse_data:
        plan_state = plan.get("state")
        plan_level = plan.get("level")

        if plan_state == "fast" and plan_level < module_plan_fast_level:
            module_plan_fast_level = plan_level

        elif plan_state == "safe" and plan_level < module_plan_safe_level:
            module_plan_safe_level = plan_level

    if module_plan_fast_level < math.inf:
        return {"state": "fast", "level": module_plan_fast_level}

    if module_plan_safe_level < math.inf:
        return {"state": "safe", "level": module_plan_safe_level}


def login_planning(login_analyse_data):
    return higher_level_planning(login_analyse_data)


def crypto_planning(crypto_analyse_data):
    return lower_level_planning(crypto_analyse_data)


def finance_planning(finance_analyse_data):
    return higher_level_planning(finance_analyse_data)


def physics_planning(physics_analyse_data):
    return higher_level_planning(physics_analyse_data)


analyse_data = get_json_inputs()

login_analyse_data = analyse_data.get("login")
crypto_analyse_data = analyse_data.get("cryptography")
finance_analyse_data = analyse_data.get("finance")
physics_analyse_data = analyse_data.get("physics")

planning_data = json.dumps(
    {
        "login": login_planning(login_analyse_data),
        "cryptography": crypto_planning(crypto_analyse_data),
        "finance": finance_planning(finance_analyse_data),
        "physics": physics_planning(physics_analyse_data),
    }
)

print(planning_data)

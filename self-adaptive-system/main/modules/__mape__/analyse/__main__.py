import json


def get_json_inputs():
    return json.loads(input())


def login_analyse(monitor_data):
    login_fail_percentage = monitor_data.get("login_fail_percentage")
    RAM_usage_percentage = monitor_data.get("RAM_usage_percentage")

    login_analyse_data = []

    if login_fail_percentage <= 100 and RAM_usage_percentage <= 100:
        login_analyse_data.append("version2")

    if login_fail_percentage <= 40 and RAM_usage_percentage <= 45:
        login_analyse_data.append("version1")

    return login_analyse_data


def crypto_analyse(monitor_data):
    network_eavesdropping_percentage = monitor_data.get(
        "network_eavesdropping_percentage"
    )

    crypto_analyse_data = []

    if network_eavesdropping_percentage <= 100:
        crypto_analyse_data.append("version4")

    if network_eavesdropping_percentage <= 80:
        crypto_analyse_data.append("version3")

    if network_eavesdropping_percentage <= 40:
        crypto_analyse_data.append("version2")

    if network_eavesdropping_percentage <= 20:
        crypto_analyse_data.append("version1")

    return crypto_analyse_data


def finance_analyse(monitor_data):
    RAM_usage_percentage = monitor_data.get("RAM_usage_percentage")
    CPU_usage_percentage = monitor_data.get("CPU_usage_percentage")

    finance_analyse_data = []

    if RAM_usage_percentage <= 100 and CPU_usage_percentage <= 100:
        finance_analyse_data.append("version1")

    if RAM_usage_percentage <= 40 and CPU_usage_percentage <= 50:
        finance_analyse_data.append("version2")

    return finance_analyse_data


def physics_analyse(monitor_data):
    RAM_usage_percentage = monitor_data.get("RAM_usage_percentage")
    CPU_usage_percentage = monitor_data.get("CPU_usage_percentage")

    physics_analyse_data = []

    if RAM_usage_percentage <= 100 and CPU_usage_percentage <= 100:
        physics_analyse_data.append("version1")

    if RAM_usage_percentage <= 80 and CPU_usage_percentage <= 90:
        physics_analyse_data.append("version2")

    if RAM_usage_percentage <= 60 and CPU_usage_percentage <= 70:
        physics_analyse_data.append("version3")

    if RAM_usage_percentage <= 20 and CPU_usage_percentage <= 30:
        physics_analyse_data.append("version4")

    return physics_analyse_data


monitor_data = get_json_inputs()

analyse_data = json.dumps(
    {
        "login": login_analyse(monitor_data),
        "cryptography": crypto_analyse(monitor_data),
        "finance": finance_analyse(monitor_data),
        "physics": physics_analyse(monitor_data),
    }
)

print(analyse_data)

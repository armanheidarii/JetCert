import json


def get_json_inputs():
    return json.loads(input())


def login_analyse(monitor_data):
    login_fail = monitor_data.get("login_fail")
    RAM_usage = monitor_data.get("RAM_usage")

    login_analyse_data = []

    if login_fail <= 100 and RAM_usage <= 100:
        login_analyse_data.append("safe_basic_auth")

    if login_fail <= 40 and RAM_usage <= 45:
        login_analyse_data.append("basic_auth")

    return login_analyse_data


def crypto_analyse(monitor_data):
    network_sniffing = monitor_data.get("network_sniffing")

    crypto_analyse_data = []

    if network_sniffing <= 100:
        crypto_analyse_data.append("rsa")

    if network_sniffing <= 80:
        crypto_analyse_data.append("triple_des")

    if network_sniffing <= 40:
        crypto_analyse_data.append("shift_cipher")

    if network_sniffing <= 20:
        crypto_analyse_data.append("wire")

    return crypto_analyse_data


def finance_analyse(monitor_data):
    RAM_usage = monitor_data.get("RAM_usage")
    CPU_usage = monitor_data.get("CPU_usage")

    finance_analyse_data = []

    if RAM_usage <= 100 and CPU_usage <= 100:
        finance_analyse_data.append("numpy_optimized")

    if RAM_usage <= 40 and CPU_usage <= 50:
        finance_analyse_data.append("numba_optimized")

    return finance_analyse_data


def physics_analyse(monitor_data):
    RAM_usage = monitor_data.get("RAM_usage")
    CPU_usage = monitor_data.get("CPU_usage")

    physics_analyse_data = []

    if RAM_usage <= 100 and CPU_usage <= 100:
        physics_analyse_data.append("numpy_optimized")

    if RAM_usage <= 80 and CPU_usage <= 90:
        physics_analyse_data.append("numba_njit_array_optimized")

    if RAM_usage <= 60 and CPU_usage <= 70:
        physics_analyse_data.append("numba_njit_scalar_optimized")

    if RAM_usage <= 20 and CPU_usage <= 30:
        physics_analyse_data.append("numba_njit_scalar_prange_optimized")

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

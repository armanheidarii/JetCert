import random
import json


def security_center():
    return {
        "CPU_usage_percentage": random.randint(0, 100),
        "RAM_usage_percentage": random.randint(0, 100),
        "login_fail_percentage": random.randint(0, 100),
        "network_eavesdropping_percentage": random.randint(0, 100),
    }


monitor_data = json.dumps(security_center())

print(monitor_data)

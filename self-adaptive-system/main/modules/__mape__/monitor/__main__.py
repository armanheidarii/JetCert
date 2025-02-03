import random
import json


def security_center():
    return {
        "CPU_usage": random.randint(0, 100),
        "RAM_usage": random.randint(0, 100),
        "login_fail": random.randint(0, 100),
        "network_sniffing": random.randint(0, 100),
    }


monitor_data = json.dumps(security_center())

print(monitor_data)

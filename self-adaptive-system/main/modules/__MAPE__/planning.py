import json
import random

print(
    json.dumps(
        {
            "login": {"state": "safe" if random.randint(0, 1) else "fast", "level": 1},
            "cryptography": {"state": "safe", "level": random.randint(1, 4)},
            "finance": {"state": "fast", "level": random.randint(1, 2)},
            "physics": {"state": "fast", "level": random.randint(1, 4)},
        }
    )
)

import json
import random

print(
    json.dumps(
        {
            "login": (
                {"state": "safe", "level": 1}
                if random.randint(0, 1)
                else {"state": "fast", "level": 1}
            ),
            "crypto": {"state": "fast", "level": 1},
        }
    )
)

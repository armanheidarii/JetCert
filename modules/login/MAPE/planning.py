import json
import random

print(
    json.dumps(
        {"state": "safe", "level": 1}
        if random.randint(0, 1) == 1
        else {"state": "fast", "level": 1}
    )
)

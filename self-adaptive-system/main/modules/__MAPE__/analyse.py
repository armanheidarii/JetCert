import json

# 5*f1+8*f2<10

print(
    json.dumps(
        {
            "choices": [
                {"state": "fast", "level": 1},
                {"state": "safe", "level": 1},
                {"state": "safe", "level": 4},
            ]
        }
    )
)

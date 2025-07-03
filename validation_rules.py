VALIDATION_RULES = [
    {
        "field": "email",
        "type": "string",
        "required": True,
        "pattern": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        "fix_strategies": [
            {"match": "missing @", "action": "insert @", "position": -1},
            {"match": "missing domain", "action": "append", "value": "@example.com"}
        ]
    },
    {
        "field": "age",
        "type": "number",
        "required": True,
        "min": 18,
        "max": 120,
        "fix_strategies": [
            {"condition": "value < min", "action": "set", "value": 18},
            {"condition": "value > max", "action": "set", "value": 120}
        ]
    }
]
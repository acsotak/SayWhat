import json
from pathlib import Path

DICT_PATH = Path(__file__).resolve().parent / "data" / "expressions.json"

with open(DICT_PATH, "r", encoding="utf-8") as file:
    expressions = json.load(file)

import re

def recognize_expression(text):
    normalized_text = text.lower().strip()

    for expression in expressions:
        pattern = r"\b" + re.escape(expression) + r"\b"

        if re.search(pattern, normalized_text):
            return expression

    return None

def get_expression(expression):
    return expressions.get(expression)


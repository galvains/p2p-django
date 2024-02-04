import re

def validator_username(value: str) -> bool:
    regex = re.compile(r"^[\w.@+-]+\Z")

    if regex.match(value):
        return False
    return True


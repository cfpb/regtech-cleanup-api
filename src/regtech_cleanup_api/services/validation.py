import re


def is_valid_cleanup_lei(lei: str = None) -> bool:
    if lei:
        return bool(re.compile(r"^[A-Z0-9]{6}E2ETEST[A-Z0-9]{5}\d{2}$").match(lei))
    return False

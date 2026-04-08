
import re


def validate_phone_number(value: str | None) -> str | None:
    if value is None:
        return None
    if not value.strip():
        return None
    if not re.match(r"^(?:(?:\+|00)86)?1\d{10}$", value):
        raise ValueError("Invalid phone number format")
    return value
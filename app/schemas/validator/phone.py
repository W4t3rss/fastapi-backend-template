
import re


def validate_phone_number(value: str | None) -> str | None:
    """
    验证手机号格式
    :param value: 待验证的手机号字符串
    :return: 验证通过的手机号字符串或 None
    :raises ValueError: 如果手机号格式不正确
    """
    if value is None:
        return None
    if not value.strip():
        return None
    if not re.match(r"^(?:(?:\+|00)86)?1\d{10}$", value):
        raise ValueError("Invalid phone number format")
    return value
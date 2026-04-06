
def validate_password(password: str, confirm_password: str) -> str:
    """
    验证密码和确认密码是否匹配
    :param password: 待验证的密码字符串
    :param confirm_password: 待验证的确认密码字符串
    :return: 验证通过的密码字符串
    :raises ValueError: 如果密码和确认密码不匹配
    """
    if password != confirm_password:
        raise ValueError("新密码和确认新密码不匹配")
    return password
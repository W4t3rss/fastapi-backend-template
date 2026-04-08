
def validate_password(password: str, confirm_password: str) -> str:
    if password != confirm_password:
        raise ValueError("Password and confirm password do not match")
    return password
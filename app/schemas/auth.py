
from typing import Literal
from pydantic import Field, ValidationInfo, field_validator
from .validator import validate_phone_number,validate_password
from .base import BaseRequest, BaseResponse

    
# Register
class Token(BaseResponse):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseRequest):
    user_name: str = Field(..., min_length=2, max_length=50, description="Username")
    phone_number: str = Field(..., max_length=20, description="Phone number")
    password: str = Field(..., min_length=6, max_length=128, description="User password")
    confirm_password: str = Field(..., min_length=6, max_length=128, description="Confirm password")
    code: str = Field(..., min_length=4, max_length=20, description="Verification code")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str | None) -> str | None:
        return validate_phone_number(value)

    @field_validator("confirm_password")
    @classmethod
    def validate_passwords(cls, value: str, info: ValidationInfo) -> str:
        password = info.data.get("password")
        if password is None:
            return value  # 如果 password 还未验证通过，先不进行 confirm_password 的验证
        validate_password(password, value)
        return value

class RegisterResponse(BaseResponse):
    id: int
    user_name: str
    phone_number: str | None
    message: str = "Registration successful"


# Login
class LoginRequest(BaseRequest):
    user_name: str = Field(..., min_length=2, max_length=50, description="Username")
    password: str = Field(..., min_length=6, max_length=128, description="User password")  

class LoginResponse(Token):
    id: int
    user_name: str
    message: str = "Login successful"


# Send Code
class SendCodeRequest(BaseRequest):
    phone_number: str = Field(..., max_length=20, description="Phone number")
    scene:Literal["register", "reset_password"] = Field(..., description="Verification code scenario: 'register' for registration, 'reset_password' for password reset")
    return_code: bool | None = Field(default=None, description="Whether to return the verification code in the response. For testing only; do not use in production")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str | None) -> str | None:
        return validate_phone_number(value)


class SendCodeResponse(BaseResponse):
    code: str | None = Field(default=None, description="Verification code. Returned only in testing when return_code is true")
    message: str = "Verification code sent"


# Reset Password
class ResetPasswordRequest(BaseRequest):
    phone_number: str | None = Field(default=None, max_length=20, description="Phone number")
    new_password: str = Field(..., min_length=6, max_length=128, description="New password")
    confirm_password: str = Field(..., min_length=6, max_length=128, description="Confirm new password")
    code: str = Field(..., min_length=4, max_length=20, description="Verification code")

    @field_validator("phone_number")
    @classmethod    
    def validate_phone_number(cls, value: str | None) -> str | None:
        return validate_phone_number(value)

    @field_validator("confirm_password")
    @classmethod
    def validate_passwords(cls, value: str, info: ValidationInfo) -> str:
        new_password = info.data.get("new_password")
        if new_password is None:
            return value
        validate_password(new_password, value)
        return value


class ResetPasswordResponse(BaseResponse):
    message: str = "Password reset successful"

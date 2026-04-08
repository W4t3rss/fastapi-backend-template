
from pydantic import BaseModel, ConfigDict


# 所有请求模型基类
class BaseRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",  
        str_strip_whitespace=True, 
    )


# 所有响应模型基类
class BaseResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        from_attributes=True,
    )



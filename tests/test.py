
from app.schemas.users import UserBase


if __name__ == "__main__":
    print(UserBase(user_name="张三", phone_number=""))
    print(UserBase(user_name="李四", phone_number=None))
    print(UserBase(user_name="王五", phone_number=""))
    print(UserBase(user_name="赵六", phone_number="+8613712345678"))

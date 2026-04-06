
from app.core.security import create_code, verify_code_expired


if __name__ == "__main__":
    
    code, expire_time = create_code()
    print(f"Generated code: {code}, expires at: {expire_time}")
    
    is_expired = verify_code_expired(expire_time)
    print(f"Is the code expired? {is_expired}")


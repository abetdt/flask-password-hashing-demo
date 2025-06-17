import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from validators import validate_email, validate_password, validate_username

def test_validate_email():
    assert validate_email("abc@example.com") == True
    assert validate_email("abc@com") == False

def test_validate_password():
    assert validate_password("abc123") == True
    assert validate_password("abc") == False
    assert validate_password("123456") == False

def test_validate_username():
    assert validate_username("user_name123") == True
    assert validate_username("invalid username") == False

if __name__ == "__main__":
    test_validate_email()
    test_validate_password()
    test_validate_username()
    print("✅ Tất cả kiểm tra validators đều thành công")

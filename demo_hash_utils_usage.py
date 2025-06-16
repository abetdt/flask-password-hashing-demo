import os
from hash_utils import set_password, verify_password

# Tạo biến môi trường giả để mô phỏng chạy trong development
os.environ["FLASK_ENV"] = "development"
os.environ["PASSWORD_PEPPER"] = "my_test_pepper_123"

def test_password_hashing_demo():
    password_plain = "MySecret123"
    
    # ✅ Hash mật khẩu
    hashed = set_password(password_plain)
    print("🔒 Hashed password:", hashed)

    # ✅ Kiểm tra đúng
    assert verify_password(password_plain, hashed) == True
    print("✅ Xác minh đúng mật khẩu thành công")

    # ❌ Kiểm tra sai
    assert verify_password("WrongPass", hashed) == False
    print("✅ Xác minh sai mật khẩu không thành công")

if __name__ == "__main__":
    test_password_hashing_demo()

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import User

def test_password_hashing():
    password = "MyPass123"
    user = User(username="test", email="test@example.com")
    user.set_password(password)

    assert user.password_hash != password, "Mật khẩu không được lưu dạng thô"
    assert user.check_password(password) == True
    assert user.check_password("sai_mat_khau") == False

if __name__ == "__main__":
    test_password_hashing()
    print("✅ Tất cả kiểm tra mật khẩu đều thành công")

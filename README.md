# Flask App: Ứng dụng Hàm Băm để Quản Lý Mật Khẩu

##  Giới thiệu

Đây là một ứng dụng web đơn giản được xây dựng bằng Flask, mô phỏng cách sử dụng hàm băm (hash function) để bảo vệ mật khẩu người dùng.

## Tính năng chính

- Đăng ký tài khoản (hash mật khẩu trước khi lưu)
- Đăng nhập (so sánh mật khẩu đã hash)
- Đăng xuất
- Giao diện web đơn giản, trực quan

##  Công nghệ sử dụng

- Python + Flask
- SQLite + SQLAlchemy
- Werkzeug Security (hash password)
- HTML/CSS (Bootstrap)

##  Cấu trúc thư mục
- app.py: Flask app chính
- models.py: CSDL - User model_
- templates/: HTML: login, register, dashboard
- static/: CSS, ảnh

# Phân công nhiệm vụ dự án

| Thành viên | Vai trò chính                       | Kết quả bàn giao                    |
|------------|-------------------------------------|-------------------------------------|
| Người 1    | Logic Flask + kết nối cơ sở dữ liệu | Ứng dụng Flask hoàn chỉnh           |
| Người 2    | Xử lý hàm băm, salt, bảo mật         | File `hash_utils.py` + các file test |
| Người 3    | Giao diện web + trải nghiệm người dùng (UX) | Template HTML, CSS               |
| Người 4    | Lý thuyết, báo cáo                  | Tài liệu Word + Slide thuyết trình  |

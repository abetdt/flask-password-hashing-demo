# Flask Password Manager

Ứng dụng quản lý mật khẩu được xây dựng bằng Flask với tính năng mã hóa bảo mật.

## Cấu trúc Project

```
flask-password-hashing-demo/
├── app/                          # Package chính của ứng dụng
│   ├── __init__.py              # Application factory
│   ├── config/                  # Cấu hình ứng dụng
│   │   ├── __init__.py
│   │   └── config.py           # Các class cấu hình
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   └── service.py          # Service model
│   ├── services/               # Business logic services
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication logic
│   │   └── password_service.py # Password management logic
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── encryption.py       # Encryption utilities
│   │   └── password_utils.py   # Password hashing utilities
│   ├── views/                  # Route handlers (Blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication routes
│   │   ├── dashboard.py       # Dashboard routes
│   │   └── services.py        # Service management routes
│   ├── static/                 # Static files (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/              # HTML templates
│       ├── auth/              # Authentication templates
│       ├── dashboard/         # Dashboard templates
│       └── services/          # Service templates
├── venv/                      # Virtual environment
├── requirements.txt           # Python dependencies
├── run.py                    # Application entry point
└── README.md                 # Project documentation
```

## Tính năng

- **Authentication**: Đăng ký, đăng nhập, đăng xuất
- **Password Management**: Thêm, sửa, xóa, xem mật khẩu
- **Encryption**: Mã hóa mật khẩu với Fernet encryption
- **Security**: Bcrypt hashing với salt và pepper
- **User Dashboard**: Quản lý dịch vụ và thống kê

## Cài đặt

1. **Tạo virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

2. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

3. **Thiết lập environment variables:**
Tạo file `.env` với các biến sau:
```env
SECRET_KEY=your-secret-key-here
PASSWORD_PEPPER=your-pepper-here
DATABASE_URL=sqlite:///password_manager.db
FLASK_ENV=development
```
4. **Sửa file .env.example thành .env:**

5. **Chạy ứng dụng:**
```bash
python run.py
```

Ứng dụng sẽ chạy tại `http://localhost:5000`

## Cấu trúc Code

### Models
- **User**: Quản lý thông tin người dùng và authentication
- **Service**: Quản lý thông tin dịch vụ và mật khẩu được mã hóa

### Services
- **AuthService**: Xử lý logic authentication
- **PasswordService**: Xử lý logic quản lý mật khẩu

### Utils
- **EncryptionService**: Mã hóa/giải mã mật khẩu với Fernet
- **Password Utils**: Hashing và verification password với bcrypt

### Views (Blueprints)
- **auth**: Routes cho authentication
- **dashboard**: Routes cho dashboard và profile
- **services**: Routes cho quản lý dịch vụ

## Bảo mật

- **Password Hashing**: Sử dụng bcrypt với salt và pepper
- **Encryption**: Fernet encryption cho mật khẩu dịch vụ
- **Session Management**: Flask session với secret key
- **Input Validation**: Kiểm tra và validate input
- **Soft Delete**: Xóa mềm thay vì xóa cứng dữ liệu

## Development

### Cấu hình Development
```python
# app/config/config.py
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///password_manager.db'
    FLASK_ENV = 'development'
```

### Logging
Ứng dụng sử dụng Python logging để ghi log các hoạt động quan trọng.

### Database
SQLite được sử dụng cho development. Có thể thay đổi sang PostgreSQL/MySQL cho production.

## Production Deployment

1. **Cấu hình Production:**
```python
# app/config/config.py
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    FLASK_ENV = 'production'
```

2. **Environment Variables:**
- `SECRET_KEY`: Secret key mạnh cho production
- `PASSWORD_PEPPER`: Pepper key cho password hashing
- `DATABASE_URL`: URL database production

3. **WSGI Server:**
Sử dụng Gunicorn hoặc uWSGI để deploy.

## Testing

Chạy tests:
```bash
python -m pytest tests/
```
## Phân công công việc nhóm

| Thành viên | Vai trò chính | Thư mục phụ trách | Công việc cụ thể | Cần tìm hiểu thêm |
|------------|---------------|-------------------|------------------|-------------------|
| **Người 1** | Backend chính *(models + services)* | `models/`, `services/`, `utils/` | - Viết và quản lý các model (user, service,...)<br>- Viết các service xử lý logic (`auth_service.py`, `password_service.py`,...)<br>- Xử lý `utils/` (mã hóa, xử lý mật khẩu,...)<br>- Viết test cho các service và logic nghiệp vụ | - `SQLAlchemy / ORM`<br>- `Clean code`, `Service layer`<br>- Unit test cơ bản |
| **Người 2** | Web routing + views *(Controller logic)* | `views/`, phối hợp `services/` | - Tạo và quản lý các route (`auth.py`, `dashboard.py`, `services.py`...)<br>- Gọi đến service và trả dữ liệu cho template<br>- Đảm bảo route đúng quy trình đăng nhập, xử lý form | - Flask routing, blueprint<br>- HTTP request/response<br>- Session, redirect, flash message |
| **Người 3** | Frontend giao diện | `templates/`, `static/` | - Thiết kế UI trong `templates/` (HTML + Jinja2)<br>- Giao diện đăng ký, đăng nhập, dashboard, profile,...<br>- Style với CSS và xử lý JavaScript đơn giản nếu có | - HTML/CSS + Bootstrap (nếu dùng)<br>- Jinja2 templating<br>- Responsive layout |
| **Người 4** | DevOps + cấu hình + quản lý config | `config/`, `instance/`, `.env`, `run.py`, `test/` | - Cấu hình Flask app, môi trường<br>- Thiết lập `.env`, `.gitignore`, `requirements.txt`<br>- Viết tài liệu `README.md` cho dự án<br>- *(Tuỳ năng lực)* viết test hoặc CI/CD (VD: GitHub Actions) | - Flask config & env<br>- Git & GitHub quản lý code team<br>- Virtualenv, pip, deploy đơn giản |



## Contributing

1. Fork project
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## License

MIT License 

from flask import Flask
from models import db, User, Service
from datetime import datetime, timezone
import os

# Setup app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # SQLite để test
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# os.environ['FLASK_ENV'] = 'development'  # Đảm bảo log hiện ra

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    # Test tạo user
    user = User(username='testuser', email='test@example.com')
    user.set_password('12345678')
    db.session.add(user)
    db.session.commit()

    # Kiểm tra verify password
    print("✅ Verify đúng:", user.verify_password('12345678'))
    print("❌ Verify sai:", user.verify_password('wrongpass'))

    # Tạo service
    service = Service(
        user_id=user.id,
        service_name='GitHub',
        service_url='https://github.com',
        service_username='gituser',
        notes='Tài khoản cá nhân'
    )
    service.set_service_password('ghp_testpassword123', master_password='12345678')
    db.session.add(service)
    db.session.commit()

    # Lấy lại password
    print("🔐 Password giải mã:", service.get_service_password(master_password='12345678'))

    # Xem dict user
    print("📦 User to_dict:", user.to_dict(include_services=True, include_stats=True))

    # Xem dict service
    print("🧾 Service to_dict:", service.to_dict(include_password=True, master_password='12345678'))

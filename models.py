from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, UTC

from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


    def set_password(self, password):
        """Hash va luu password"""
        if not password:
            raise ValueError("Password khong duoc de trong")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Kiem tra password"""
        if not password:
            return False
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Cap nhat thoi gian dang nhap lan cuoi"""
        self.last_login = datetime.now(UTC)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        """Chuyen doi thanh dictionary"""
        user_dict = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.created_at else None,
            "is_active": self.is_active
        }
        return user_dict

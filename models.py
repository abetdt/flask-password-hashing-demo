

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import os #Kiem tra moi truong chay
import logging
from typing import Optional
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()  # Tự động load từ file .env

db = SQLAlchemy()
def kiem_tra_moi_truong_chay() -> bool:
    return os.getenv("FLASK_ENV") == "development"

def get_password_pepper() -> str:
    """
    Lấy pepper từ environment variable
    Pepper là một secret key cố định dùng để tăng cường bảo mật password
    """
    pepper = os.getenv("PASSWORD_PEPPER")
    if not pepper:
        if kiem_tra_moi_truong_chay():
            logger.warning("PASSWORD_PEPPER not found in environment variables, using default for development")
            return "dev_pepper_2025_abetdt_secret_key"
        else:
            raise ValueError("PASSWORD_PEPPER environment variable is required in production")
    return pepper
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    services = db.relationship('Service', backref='user', lazy=True, cascade='all, delete-orphan')

    def _add_pepper_to_password(self, password: str) -> str:
        """
        Thêm pepper vào password trước khi hash
        Pepper được thêm vào cuối password để tăng cường bảo mật
        """
        try:
            pepper = get_password_pepper()
            # Combine password với pepper
            peppered_password = password + pepper

            if kiem_tra_moi_truong_chay():
                logger.debug(f"Added pepper to password for user: {self.username}")
                logger.debug(f"Original password length: {len(password)}")
                logger.debug(f"Peppered password length: {len(peppered_password)}")

            return peppered_password
        except Exception as e:
            logger.error(f"Error adding pepper to password: {e}")
            raise

    #Method set password xuong database
    def set_password(self, password):
        """
        Hash password với bcrypt + salt + pepper

        Args:
            password (str): Plain text password

        Raises:
            ValueError: Nếu password rỗng
            Exception: Nếu có lỗi trong quá trình hash
        """
        if not password:
            raise ValueError("Password cannot be empty")

        try:
            # Bước 1: Thêm pepper vào password
            peppered_password = self._add_pepper_to_password(password)
            # Sinh salt ngẫu nhiên
            salt = bcrypt.gensalt()
            print(f"Salt được tạo: {salt}")
            print(f"Độ dài salt: {len(salt)} bytes")

            #Log de thay ro khi chay o moi truong development
            if kiem_tra_moi_truong_chay():
                logger.debug(f"Generated salt for user: {self.username}")
                logger.debug(f"Salt: {salt}")
                logger.debug(f"Salt length: {len(salt)} bytes")

            #Hash password
            # Chuyển password thành bytes
            peppered_password_bytes = peppered_password.encode('utf-8')
            hashed = bcrypt.hashpw(peppered_password_bytes, salt)
            #Luu database dang string
            self.password_hash = hashed.decode('utf-8')

            #Log hash structure
            if kiem_tra_moi_truong_chay():
                logger.debug(f"Password hashed successfully for user: {self.username}")
                logger.debug(f"Hash length: {len(self.password_hash)}")
                logger.debug(f"Salt in hash: {self.password_hash[:29]}")
                logger.debug(f"Same salt: {salt.decode('utf-8') == self.password_hash[:29]} ")
        except Exception as e:
            logger.error(f"Error setting password for user {self.username}: {e}")
            raise
    def verify_password(self, password: str) ->bool:
        """
        Verify password với bcrypt + pepper

        Args:
            password (str): Plain text password để verify

        Returns:
            bool: True nếu password đúng, False nếu sai
        """
        if not password or not self.password_hash:
            return False
        try:
            # Bước 1: Thêm pepper vào password input
            peppered_password = self._add_pepper_to_password(password)
            # Bước 2: Convert sang bytes
            peppered_password_bytes = peppered_password.encode('utf-8')
            stored_hash = self.password_hash.encode('utf-8')
            # Bước 3: Verify với bcrypt
            is_valid = bcrypt.checkpw(peppered_password_bytes, stored_hash)
            if kiem_tra_moi_truong_chay():
                logger.debug(f"Password verification for user {self.username}: {'SUCCESS' if is_valid else 'FAILED'}")
            return is_valid
        except Exception as e:
            logger.error(f"Error verifying password for user {self.username}: {e}")
            return False
    @property
    def salt_from_hash(self):
        """Extract salt từ hash (chỉ để xem)"""
        return self.password_hash[:29] if self.password_hash else None

    def to_dict(self, include_services=False, include_stats=False):
        """
                Chuyển đổi User object thành dictionary

                Args:
                    include_services (bool): Có include danh sách services không
                    include_stats (bool): Có include thống kê không

                Returns:
                    dict: User data (KHÔNG bao gồm password_hash)
        """
        user_dict = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

        # Thêm services nếu được yêu cầu
        # Query services thay vì dùng relationship trực tiếp
        if include_services:
            try:
                from sqlalchemy.orm import sessionmaker
                # Lấy tất cả các service đang hoạt động (is_active=True) của user này từ database
                active_services = db.session.query(Service).filter(
                    Service.user_id == self.id,
                    Service.is_active == True
                ).all()

                # Chuyển từng service thành dictionary để có thể trả về dạng JSON
                # Tạo danh sách trống để chứa các service dạng dict
                services_list = []
                for service in active_services:
                    service_dict = service.to_dict()
                    services_list.append(service_dict)
                user_dict["services"] = services_list
                #Gon hon
                # user_dict["services"] = [
                #     service.to_dict() for service in active_services]
            except Exception as e:
                logger.error(f"Error loading services for user {self.username}: {e}")
                user_dict["services"] = []

        # Thêm stats nếu được yêu cầu
        if include_stats:
            try:
                total_services = db.session.query(Service).filter(
                    Service.user_id == self.id
                ).count()
                active_services_count = db.session.query(Service).filter(
                    Service.user_id == self.id,
                    Service.is_active == True,
                ).count()
                account_age_days = 0
                if self.created_at:
                    now = datetime.utcnow()
                    created_at_tmp = self.created_at
                    account_age_days = (now - created_at_tmp).days
                user_dict["stats"] = {
                    "total_services": total_services,
                    "active_services": active_services_count,
                    "account_age_days":account_age_days
                }
            except Exception as e:
                logger.error(f"Error calculating stats for user {self.username}: {e}")
                user_dict["stats"] = {
                    "total_services": 0,
                    "active_services": 0,
                    "account_age_days": 0
                }
        return user_dict

    def to_public_dict(self):
        """Version công khai (ít thông tin hơn)"""
        return {
            "id": self.id,
            "username": self.username,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def find_by_username(cls, username: str) -> Optional['User']:
        """Tìm user theo username"""
        return cls.query.filter_by(username=username, is_active=True).first()

    @classmethod
    def find_by_email(cls, email: str) -> Optional['User']:
        """Tìm user theo email"""
        return cls.query.filter_by(email=email, is_active=True).first()
    def __repr__(self):
        return f"<User {self.username}>"


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    #User_id la foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    service_name = db.Column(db.String(100), nullable=False)
    service_url = db.Column(db.String(255))
    service_username = db.Column(db.String(100), nullable=False)
    service_password_encrypted = db.Column(db.Text, nullable=False)
    encryption_salt = db.Column(db.String(32), nullable=False)
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_password=False, master_password=None):
        """
        Chuyển đổi Service object thành dictionary

        Args:
            include_password (bool): Có include password đã decrypt không
            master_password (str): Master password để decrypt (nếu cần)

        Returns:
            dict: Service data
        """
        service_dict = {
            "id": self.id,
            "service_name": self.service_name,
            "service_url": self.service_url,
            "service_username": self.service_username,
            "notes": self.notes,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id
        }

        # Thêm password đã decrypt nếu được yêu cầu và có master password
        if include_password and master_password:
            try:
                decrypted_password = self.get_service_password(master_password)
                service_dict["service_password"] = decrypted_password
            except Exception as e:
                service_dict["service_password"] = None
                service_dict["password_error"] = "Could not decrypt password"

        return service_dict

    def to_summary_dict(self):
        """Version tóm tắt (không có password)"""
        return {
            "id": self.id,
            "service_name": self.service_name,
            "service_url": self.service_url,
            "service_username": self.service_username,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


    def set_service_password(self, password: str, master_password: str):
        """Encrypt service password"""
        from ecryption_password import EncryptionService
        encryptor = EncryptionService(master_password)
        self.service_password_encrypted = encryptor.encrypt(password)
        self.encryption_salt = encryptor.get_salt()

    def get_service_password(self, master_password):
        """Decrypt service password"""
        from ecryption_password import EncryptionService
        try:
            encryptor = EncryptionService(master_password, salt=self.encryption_salt)
            return encryptor.decrypt(self.service_password_encrypted)
        except Exception:
            return None  # Hoặc raise custom exception nếu cần

    def __repr__(self):
        return f'<Service {self.service_name} for {self.user.username}>'



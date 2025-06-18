"""
Service model for password management
"""
from datetime import datetime
from typing import Optional, Dict, Any
from app import db
from app.utils.encryption import EncryptionService
import logging

logger = logging.getLogger(__name__)

class Service(db.Model):
    """Service model for storing encrypted passwords"""
    
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
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

    def to_dict(self, include_password: bool = False, master_password: str = None) -> Dict[str, Any]:
        """
        Convert Service object to dictionary
        
        Args:
            include_password (bool): Include decrypted password
            master_password (str): Master password for decryption (if needed)
            
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

        # Add decrypted password if requested and master password provided
        if include_password and master_password:
            try:
                decrypted_password = self.get_service_password(master_password)
                service_dict["service_password"] = decrypted_password
            except Exception as e:
                service_dict["service_password"] = None
                service_dict["password_error"] = "Could not decrypt password"
                logger.error(f"Error decrypting password for service {self.id}: {e}")

        return service_dict

    def to_summary_dict(self) -> Dict[str, Any]:
        """Summary version without password"""
        return {
            "id": self.id,
            "service_name": self.service_name,
            "service_url": self.service_url,
            "service_username": self.service_username,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def set_service_password(self, password: str, master_password: str) -> None:
        """
        Encrypt and set service password
        
        Args:
            password (str): Plain text password to encrypt
            master_password (str): Master password for encryption
        """
        if not password:
            raise ValueError("Password cannot be empty")
            
        if not master_password:
            raise ValueError("Master password cannot be empty")
            
        try:
            encryptor = EncryptionService(master_password)
            self.service_password_encrypted = encryptor.encrypt(password)
            self.encryption_salt = encryptor.get_salt()
            logger.debug(f"Password encrypted successfully for service {self.id}")
        except Exception as e:
            logger.error(f"Error encrypting password for service {self.id}: {e}")
            raise

    def get_service_password(self, master_password: str) -> Optional[str]:
        """
        Decrypt service password
        
        Args:
            master_password (str): Master password for decryption
            
        Returns:
            str: Decrypted password, or None if decryption fails
        """
        if not master_password:
            raise ValueError("Master password cannot be empty")
            
        if not self.service_password_encrypted or not self.encryption_salt:
            return None
            
        try:
            encryptor = EncryptionService(master_password, salt=self.encryption_salt)
            decrypted = encryptor.decrypt(self.service_password_encrypted)
            logger.debug(f"Password decrypted successfully for service {self.id}")
            return decrypted
        except Exception as e:
            logger.error(f"Error decrypting password for service {self.id}: {e}")
            return None

    def __repr__(self) -> str:
        return f'<Service {self.service_name} for user {self.user_id}>' 
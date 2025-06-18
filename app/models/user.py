"""
User model for authentication and user management
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from app import db
from app.utils.password_utils import hash_password, verify_password
import logging

logger = logging.getLogger(__name__)

class User(db.Model):
    """User model for authentication and user management"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    services = db.relationship('Service', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str) -> None:
        """
        Set user password with hashing
        
        Args:
            password (str): Plain text password
            
        Raises:
            ValueError: If password is empty
            Exception: If error occurs during hashing
        """
        if not password:
            raise ValueError("Password cannot be empty")
            
        try:
            self.password_hash = hash_password(password)
            logger.debug(f"Password set successfully for user: {self.username}")
        except Exception as e:
            logger.error(f"Error setting password for user {self.username}: {e}")
            raise

    def verify_password(self, password: str) -> bool:
        """
        Verify user password
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password is correct, False otherwise
        """
        if not password or not self.password_hash:
            return False
            
        try:
            is_valid = verify_password(password, self.password_hash)
            logger.debug(f"Password verification for user {self.username}: {'SUCCESS' if is_valid else 'FAILED'}")
            return is_valid
        except Exception as e:
            logger.error(f"Error verifying password for user {self.username}: {e}")
            return False

    @property
    def salt_from_hash(self) -> Optional[str]:
        """Extract salt from hash (for debugging purposes only)"""
        return self.password_hash[:29] if self.password_hash else None

    def to_dict(self, include_services: bool = False, include_stats: bool = False) -> Dict[str, Any]:
        """
        Convert User object to dictionary
        
        Args:
            include_services (bool): Include list of services
            include_stats (bool): Include user statistics
            
        Returns:
            dict: User data (excluding password_hash)
        """
        user_dict = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

        # Add services if requested
        if include_services:
            try:
                from app.models.service import Service
                active_services = db.session.query(Service).filter(
                    Service.user_id == self.id,
                    Service.is_active == True
                ).all()
                
                services_list = [service.to_dict() for service in active_services]
                user_dict["services"] = services_list
            except Exception as e:
                logger.error(f"Error loading services for user {self.username}: {e}")
                user_dict["services"] = []

        # Add stats if requested
        if include_stats:
            try:
                from app.models.service import Service
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
                    account_age_days = (now - self.created_at).days
                    
                user_dict["stats"] = {
                    "total_services": total_services,
                    "active_services": active_services_count,
                    "account_age_days": account_age_days
                }
            except Exception as e:
                logger.error(f"Error calculating stats for user {self.username}: {e}")
                user_dict["stats"] = {
                    "total_services": 0,
                    "active_services": 0,
                    "account_age_days": 0
                }
                
        return user_dict

    def to_public_dict(self) -> Dict[str, Any]:
        """Public version with limited information"""
        return {
            "id": self.id,
            "username": self.username,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def find_by_username(cls, username: str) -> Optional['User']:
        """Find user by username"""
        return cls.query.filter_by(username=username, is_active=True).first()

    @classmethod
    def find_by_email(cls, email: str) -> Optional['User']:
        """Find user by email"""
        return cls.query.filter_by(email=email, is_active=True).first()

    def __repr__(self) -> str:
        return f"<User {self.username}>" 
"""
Authentication service for user management
"""
from typing import Optional, Tuple
from flask import session
from app.models.user import User
from app import db
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """Service for handling authentication logic"""
    
    @staticmethod
    def login_user(username: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Authenticate user login
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            tuple: (success, error_message)
        """
        try:
            user = User.find_by_username(username)
            if user and user.verify_password(password):
                session['user_id'] = user.id
                logger.info(f"User {username} logged in successfully")
                return True, None
            else:
                logger.warning(f"Failed login attempt for username: {username}")
                return False, "Tên đăng nhập hoặc mật khẩu sai."
        except Exception as e:
            logger.error(f"Error during login for user {username}: {e}")
            return False, "Có lỗi xảy ra trong quá trình đăng nhập."

    @staticmethod
    def register_user(username: str, email: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Register new user
        
        Args:
            username (str): Username
            email (str): Email
            password (str): Password
            
        Returns:
            tuple: (success, error_message)
        """
        try:
            # Check if user already exists
            if User.find_by_username(username):
                return False, "Tên đăng nhập đã tồn tại."
                
            if User.find_by_email(email):
                return False, "Email đã tồn tại."
            
            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            logger.info(f"User {username} registered successfully")
            return True, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error registering user {username}: {e}")
            return False, "Có lỗi xảy ra trong quá trình đăng ký."

    @staticmethod
    def logout_user() -> None:
        """Logout current user"""
        user_id = session.pop('user_id', None)
        if user_id:
            logger.info(f"User {user_id} logged out")

    @staticmethod
    def get_current_user() -> Optional[User]:
        """
        Get current logged in user
        
        Returns:
            User: Current user object or None if not logged in
        """
        user_id = session.get('user_id')
        if user_id:
            return User.query.get(user_id)
        return None

    @staticmethod
    def is_authenticated() -> bool:
        """
        Check if user is authenticated
        
        Returns:
            bool: True if user is logged in
        """
        return 'user_id' in session 
"""
Password utilities for hashing and verification
"""
import bcrypt
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def get_password_pepper() -> str:
    """
    Get pepper from environment variable
    Pepper is a fixed secret key used to enhance password security
    
    Returns:
        str: Password pepper
    """
    pepper = os.getenv("PASSWORD_PEPPER")
    if not pepper:
        # Always use default pepper for development
        logger.warning("PASSWORD_PEPPER not found in environment variables, using default for development")
        return "dev_pepper_2025_abetdt_secret_key"
    return pepper

def is_development_environment() -> bool:
    """
    Check if running in development environment
    
    Returns:
        bool: True if development environment
    """
    return os.getenv("FLASK_ENV") == "development" or os.getenv("FLASK_ENV") is None

def add_pepper_to_password(password: str) -> str:
    """
    Add pepper to password before hashing
    Pepper is added to the end of password to enhance security
    
    Args:
        password (str): Original password
        
    Returns:
        str: Password with pepper added
    """
    try:
        pepper = get_password_pepper()
        peppered_password = password + pepper
        
        if is_development_environment():
            logger.debug(f"Added pepper to password")
            logger.debug(f"Original password length: {len(password)}")
            logger.debug(f"Peppered password length: {len(peppered_password)}")
            
        return peppered_password
    except Exception as e:
        logger.error(f"Error adding pepper to password: {e}")
        raise

def hash_password(password: str) -> str:
    """
    Hash password using bcrypt with salt and pepper
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
        
    Raises:
        ValueError: If password is empty
        Exception: If error occurs during hashing
    """
    if not password:
        raise ValueError("Password cannot be empty")
        
    try:
        # Add pepper to password
        peppered_password = add_pepper_to_password(password)
        
        # Generate random salt
        salt = bcrypt.gensalt()
        
        if is_development_environment():
            logger.debug(f"Generated salt")
            logger.debug(f"Salt: {salt}")
            logger.debug(f"Salt length: {len(salt)} bytes")
        
        # Hash password
        peppered_password_bytes = peppered_password.encode('utf-8')
        hashed = bcrypt.hashpw(peppered_password_bytes, salt)
        
        # Store as string
        password_hash = hashed.decode('utf-8')
        
        if is_development_environment():
            logger.debug(f"Password hashed successfully")
            logger.debug(f"Hash length: {len(password_hash)}")
            logger.debug(f"Salt in hash: {password_hash[:29]}")
            
        return password_hash
        
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise

def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify password against stored hash
    
    Args:
        password (str): Plain text password to verify
        password_hash (str): Stored password hash
        
    Returns:
        bool: True if password is correct, False otherwise
    """
    if not password or not password_hash:
        return False
        
    try:
        # Add pepper to input password
        peppered_password = add_pepper_to_password(password)
        
        # Convert to bytes
        peppered_password_bytes = peppered_password.encode('utf-8')
        stored_hash = password_hash.encode('utf-8')
        
        # Verify with bcrypt
        is_valid = bcrypt.checkpw(peppered_password_bytes, stored_hash)
        
        if is_development_environment():
            logger.debug(f"Password verification: {'SUCCESS' if is_valid else 'FAILED'}")
            
        return is_valid
        
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False

def extract_salt_from_hash(password_hash: str) -> Optional[str]:
    """
    Extract salt from hash (for debugging purposes only)
    
    Args:
        password_hash (str): Password hash
        
    Returns:
        str: Salt from hash, or None if invalid
    """
    return password_hash[:29] if password_hash else None 
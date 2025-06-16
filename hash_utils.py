
import bcrypt
import os
import logging

from dotenv import load_dotenv
load_dotenv()  # Load biến môi trường từ file .env

logger = logging.getLogger(__name__)

def kiem_tra_moi_truong_chay() -> bool:
    return os.getenv("FLASK_ENV") == "development"

def get_password_pepper() -> str:
    pepper = os.getenv("PASSWORD_PEPPER")
    if not pepper:
        if kiem_tra_moi_truong_chay():
            logger.warning("PASSWORD_PEPPER not found, using development default")
            return "dev_pepper_2025_abetdt_secret_key"
        else:
            raise ValueError("PASSWORD_PEPPER environment variable is required in production")
    return pepper

def _add_pepper_to_password(password: str) -> str:
    try:
        pepper = get_password_pepper()
        peppered_password = password + pepper

        if kiem_tra_moi_truong_chay():
            logger.debug(f"Original password length: {len(password)}")
            logger.debug(f"Peppered password length: {len(peppered_password)}")

        return peppered_password
    except Exception as e:
        logger.error(f"Error adding pepper: {e}")
        raise

def set_password(password: str) -> str:
    if not password:
        raise ValueError("Password cannot be empty")
    try:
        peppered = _add_pepper_to_password(password)
        salt = bcrypt.gensalt()
        print(f"Salt được tạo: {salt}")
        print(f"Độ dài salt: {len(salt)} bytes")
        hashed = bcrypt.hashpw(peppered.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise

def verify_password(password: str, hashed_password: str) -> bool:
    if not password or not hashed_password:
        return False
    try:
        peppered = _add_pepper_to_password(password)
        is_valid = bcrypt.checkpw(peppered.encode('utf-8'), hashed_password.encode('utf-8'))
        return is_valid
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False

"""
Encryption utilities for password management
"""
import base64
import secrets
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)

class EncryptionService:
    """
    Service for encrypting and decrypting sensitive data using Fernet encryption
    """
    
    def __init__(self, master_password: str, salt: str = None):
        """
        Initialize encryption service with master password
        
        Args:
            master_password (str): Master password for encryption/decryption
            salt (str, optional): Salt for key derivation. If None, generates new salt
        """
        if not master_password:
            raise ValueError("Master password cannot be empty")
            
        self.master_password = master_password
        self.salt = salt or secrets.token_hex(16)
        self._key = self._derive_key()

    def _derive_key(self) -> bytes:
        """
        Derive encryption key from master password using PBKDF2
        
        Returns:
            bytes: Derived encryption key
        """
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt.encode(),
                iterations=100000,
            )
            return base64.urlsafe_b64encode(kdf.derive(self.master_password.encode()))
        except Exception as e:
            logger.error(f"Error deriving key: {e}")
            raise

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using Fernet encryption
        
        Args:
            plaintext (str): Text to encrypt
            
        Returns:
            str: Encrypted text
        """
        if not plaintext:
            raise ValueError("Plaintext cannot be empty")
            
        try:
            f = Fernet(self._key)
            encrypted = f.encrypt(plaintext.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Error encrypting text: {e}")
            raise

    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypt encrypted text using Fernet decryption
        
        Args:
            encrypted_text (str): Text to decrypt
            
        Returns:
            str: Decrypted text
        """
        if not encrypted_text:
            raise ValueError("Encrypted text cannot be empty")
            
        try:
            f = Fernet(self._key)
            decrypted = f.decrypt(encrypted_text.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Error decrypting text: {e}")
            raise

    def get_salt(self) -> str:
        """
        Get the salt used for key derivation
        
        Returns:
            str: Salt string
        """
        return self.salt 
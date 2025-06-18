# encryption.py
import base64
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptionService:
    def __init__(self, master_password: str, salt: str = None):
        """
        Args:
            master_password (str): Mật khẩu chính của người dùng.
            salt (str | None): Salt hex string. Nếu None thì tự tạo mới.
        """
        self.master_password = master_password
        self.salt = salt or secrets.token_hex(16)  # Tạo salt mới nếu chưa có
        self._key = self._derive_key()

    def _derive_key(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt.encode(),
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(self.master_password.encode()))

    def encrypt(self, plaintext: str) -> str:
        f = Fernet(self._key)
        return f.encrypt(plaintext.encode()).decode()

    def decrypt(self, encrypted_text: str) -> str:
        f = Fernet(self._key)
        return f.decrypt(encrypted_text.encode()).decode()

    def get_salt(self):
        return self.salt

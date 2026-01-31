import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from cryptography.fernet import Fernet
from pydantic import BaseModel

# Configuration
SECRET_KEY = "CHANGE_THIS_IN_PRODUCTION_TO_A_LONG_RANDOM_STRING"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 Days

# Encryption Key Management
KEY_FILE = "secret.key"

def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

ENCRYPTION_KEY = load_or_create_key()
cipher_suit = Fernet(ENCRYPTION_KEY)

class TokenData(BaseModel):
    email: Optional[str] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return TokenData(email=email)
    except JWTError:
        return None

def encrypt_password(password: str) -> str:
    return cipher_suit.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    return cipher_suit.decrypt(encrypted_password.encode()).decode()

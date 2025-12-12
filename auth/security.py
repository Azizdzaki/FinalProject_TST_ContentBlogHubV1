from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.user import UserInDB
from database.db import mock_users


# Konfigurasi JWT
SECRET_KEY = "kunci_rahasia_sangat_aman_untuk_tugas_besar_ini"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Skema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, stored_password):
    """Verifikasi password sederhana"""
    return plain_password == stored_password


def get_password_hash(password):
    """Hash password (untuk referensi)"""
    return password


def get_user(db, username: str):
    """Ambil user dari database"""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validasi token dan ambil user"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )

    user = get_user(mock_users, username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.user import Token
from database.db import mock_users 
from auth.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password, get_user

router = APIRouter(tags=["Authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Cari user di database mock
    user = get_user(mock_users, form_data.username)
    
    # 2. Verifikasi user dan password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Jika valid, buat token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # 4. Kembalikan token ke pengguna
    return {"access_token": access_token, "token_type": "bearer"}
# app/core/config.py
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("SECRET_KEY", "wZ33g4zndyB7qnGIo52dTueg")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30

# Mova o contexto do bcrypt para cá
bcryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mova o esquema OAuth2 para cá
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-from")
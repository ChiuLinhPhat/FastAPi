from typing import Annotated
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "bcb75c2e5e8b4ab5c2b9f4fb754d1cab409b0eca26d1f774428924b07fb7f5db"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv
import secrets

load_dotenv()

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("API_USER")
    correct_password = os.getenv("API_PASSWORD")

    username_match = secrets.compare_digest(credentials.username, correct_username)
    password_match = secrets.compare_digest(credentials.password, correct_password)

    if not (username_match and password_match):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username

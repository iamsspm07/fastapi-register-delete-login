import re
import bcrypt
import logging
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Secret key and algorithm for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    """Hashes the given password using bcrypt with exception handling."""
    try:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    except Exception as e:
        logging.error(f"Error hashing password: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while hashing password.")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against its hashed version with exception handling."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception as e:
        logging.error(f"Error verifying password: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while verifying password.")

def validate_password(password: str):
    """Validates password complexity using regex."""
    try:
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        if not re.fullmatch(pattern, password):
            raise ValueError("Password must be at least 8 characters, include letters, numbers, and a special symbol.")
    except Exception as e:
        logging.error(f"Password validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def validate_email(email: str):
    """Validates email format using regex."""
    try:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.fullmatch(pattern, email):
            raise ValueError("Invalid email format.")
    except Exception as e:
        logging.error(f"Email validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def validate_phone(phone: str):
    """Validates phone number format (10 digits, starting with 6-9)."""
    try:
        if not re.fullmatch(r"^[6-9]\d{9}$", phone):
            raise ValueError("Invalid phone number format. Must be a 10-digit number starting with 6-9.")
    except Exception as e:
        logging.error(f"Phone validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    """Generates a JWT access token with exception handling."""
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except JWTError as e:
        logging.error(f"Error creating JWT token: {e}")
        raise HTTPException(status_code=500, detail="Error generating access token.")
    except Exception as e:
        logging.error(f"Unexpected error creating access token: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while generating access token.")

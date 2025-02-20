# import logging
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import SQLAlchemyError
# from datetime import timedelta
# from database import get_db
# from schemas import UserRegistrationRequest, UserLoginRequest, TokenResponse
# from crud import create_user, authenticate_user, delete_user_by_phone
# from utils import create_access_token
# from config import settings

# # Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# router = APIRouter()

# @router.post("/register/", response_model=dict)
# def register_user(user_data: UserRegistrationRequest, db: Session = Depends(get_db)):
#     """
#     Registers a new user in the system.
#     Returns a success message along with the user ID.
#     """
#     try:
#         user_id = create_user(db, user_data)
#         if not user_id:
#             raise HTTPException(status_code=400, detail="Invalid role or profession.")
        
#         logging.info(f"✅ User registered successfully: {user_data.email}")
#         return {"message": "User registered successfully!", "user_id": user_id}

#     except SQLAlchemyError as e:
#         logging.error(f"❌ Database error during registration: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error.")
    
#     except Exception as e:
#         logging.error(f"❌ Unexpected error: {str(e)}")
#         raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# @router.post("/login/", response_model=TokenResponse)
# def login(user_data: UserLoginRequest, db: Session = Depends(get_db)):
#     """
#     Authenticates a user and returns an access token if credentials are valid.
#     """
#     try:
#         user = authenticate_user(db, user_data.email, user_data.password)
#         if not user:
#             logging.warning(f"⚠ Login failed: Invalid credentials for {user_data.email}")
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
        
#         access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = create_access_token(data={"sub": user.user_mail}, expires_delta=access_token_expires)

#         logging.info(f"✅ User logged in successfully: {user_data.email}")
#         return {"access_token": access_token, "token_type": "bearer"}

#     except SQLAlchemyError as e:
#         logging.error(f"❌ Database error during login: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error.")
    
#     except Exception as e:
#         logging.error(f"❌ Unexpected error: {str(e)}")
#         raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# @router.delete("/delete/{phone_number}/", response_model=dict)
# def delete_user(phone_number: str, db: Session = Depends(get_db)):
#     """
#     Deletes a user by phone number from the database.
#     """
#     try:
#         success = delete_user_by_phone(db, phone_number)
#         if not success:
#             logging.warning(f"⚠ User deletion failed: No user found for phone {phone_number}")
#             raise HTTPException(status_code=404, detail="User not found")

#         logging.info(f"✅ User deleted successfully: {phone_number}")
#         return {"message": "User deleted successfully!"}

#     except SQLAlchemyError as e:
#         logging.error(f"❌ Database error during deletion: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error.")
    
#     except Exception as e:
#         logging.error(f"❌ Unexpected error: {str(e)}")
#         raise HTTPException(status_code=500, detail="An unexpected error occurred.")



import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta
from database import get_db
from schemas import UserRegistrationRequest, UserLoginRequest, TokenResponse
from crud import create_user, authenticate_user, delete_user_by_phone
from utils import create_access_token
from config import settings
from schemas import UserDeleteRequest  # Import it from schemas.py


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

router = APIRouter()

@router.post("/register/", response_model=dict)
def register_user(user_data: UserRegistrationRequest, db: Session = Depends(get_db)):
    """
    Registers a new user in the system.
    Returns a success message along with the user ID.
    """
    try:
        user_id = create_user(db, user_data)
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid role or profession.")
        
        logging.info(f"✅ User registered successfully: {user_data.email}")
        return {"message": "User registered successfully!", "user_id": user_id}

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
    
    except Exception as e:
        logging.error(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.post("/login/", response_model=TokenResponse)
def login(user_data: UserLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns an access token if credentials are valid.
    """
    try:
        user = authenticate_user(db, user_data.email, user_data.password)
        if not user:
            logging.warning(f"⚠ Login failed: Invalid credentials for {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.user_mail}, expires_delta=access_token_expires)

        logging.info(f"✅ User logged in successfully: {user_data.email}")
        return {"access_token": access_token, "token_type": "bearer"}

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
    
    except Exception as e:
        logging.error(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.delete("/delete/", response_model=dict)
def delete_user(user_data: UserDeleteRequest, db: Session = Depends(get_db)):
    """
    Deletes a user by phone number from the database.
    """
    try:
        phone_number = user_data.phone  # Extract phone number from request body
        success = delete_user_by_phone(db, phone_number)

        if not success:
            logging.warning(f"⚠ User deletion failed: No user found for phone {phone_number}")
            raise HTTPException(status_code=404, detail="User not found")

        logging.info(f"✅ User deleted successfully: {phone_number}")
        return {"message": "User deleted successfully!"}

    except Exception as e:
        logging.error(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
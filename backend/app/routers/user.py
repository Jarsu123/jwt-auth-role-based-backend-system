from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..deps import get_db
from ..auth import hash_password, verify_password, create_token
import logging

# Setup logger for this module
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        logger.warning(f"Registration attempt with existing email: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already exists"
        )

    new_user = models.User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"New user registered: {user.email}")
    return {"msg": "User created successfully"}

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        logger.warning(f"Failed login attempt for email: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )

    token = create_token({"user_id": db_user.id})

    logger.info(f"User logged in: {user.email} (Role: {db_user.role})")
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": db_user
    }
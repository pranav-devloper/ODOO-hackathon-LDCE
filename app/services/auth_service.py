from datetime import datetime, timedelta
import uuid
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.models import User
from app.core.security import verify_password, get_password_hash, create_access_token

def signup(db: Session, name: str, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise ValueError("Email already registered")
    
    password_hash = get_password_hash(password)
    new_user = User(
        name=name,
        email=email,
        password_hash=password_hash
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Failed to create user")

def login(db: Session, email: str, password: str) -> Tuple[User, str]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("Invalid email or password")
    
    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password")
    
    token = create_access_token(data={"sub": str(user.id)})
    return user, token

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)
            
    db.commit()
    db.refresh(user)
    return user

def generate_reset_token(db: Session, email: str) -> str:
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("User not found")
    # For hackathon: just return a UUID token
    return str(uuid.uuid4())

def reset_password(db: Session, email: str, new_password: str) -> bool:
    user = get_user_by_email(db, email)
    if not user:
        return False
    
    user.password_hash = get_password_hash(new_password)
    db.commit()
    return True

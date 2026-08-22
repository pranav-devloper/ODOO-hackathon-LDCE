from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.security import decode_access_token
from app.database.models import User

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    token = request.cookies.get("access_token")
    if not token:
        return None
        
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
        
    payload = decode_access_token(token)
    if not payload:
        return None
        
    user_id: str = payload.get("sub")
    if user_id is None:
        return None
        
    user = db.query(User).filter(User.id == int(user_id)).first()
    return user

def get_current_user_required(current_user: User = Depends(get_current_user)) -> User:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return current_user

def get_admin_user(current_user: User = Depends(get_current_user_required)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    return current_user

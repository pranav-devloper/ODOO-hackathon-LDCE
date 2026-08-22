from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.auth import SignupRequest, LoginRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.services import auth_service
from app.core.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/signup")
def signup(request: SignupRequest, response: Response, db: Session = Depends(get_db)):
    try:
        if request.password != request.confirm_password:
            return {"success": False, "data": None, "error": {"code": "PASSWORD_MISMATCH", "message": "Passwords do not match"}}
        user = auth_service.signup(db, request.name, request.email, request.password)
        token = create_access_token(data={"sub": str(user.id)})
        response.set_cookie(key="access_token", value=token, httponly=True, samesite="lax", max_age=86400)
        return {"success": True, "data": {"user_id": user.id, "name": user.name}, "error": None}
    except ValueError as e:
        return {"success": False, "data": None, "error": {"code": "SIGNUP_FAILED", "message": str(e)}}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "SIGNUP_ERROR", "message": str(e)}}

@router.post("/login")
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    try:
        user, token = auth_service.login(db, request.email, request.password)
        response.set_cookie(key="access_token", value=token, httponly=True, samesite="lax", max_age=86400)
        return {"success": True, "data": {"user_id": user.id, "name": user.name}, "error": None}
    except ValueError as e:
        return {"success": False, "data": None, "error": {"code": "LOGIN_FAILED", "message": str(e)}}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "LOGIN_ERROR", "message": str(e)}}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"success": True, "data": None, "error": None}

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    try:
        token = auth_service.generate_reset_token(db, request.email)
        return {"success": True, "data": {"reset_token": token, "message": "In development mode, use this token to reset your password."}, "error": None}
    except ValueError as e:
        return {"success": False, "data": None, "error": {"code": "FORGOT_PASSWORD_FAILED", "message": str(e)}}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        if request.new_password != request.confirm_password:
            return {"success": False, "data": None, "error": {"code": "PASSWORD_MISMATCH", "message": "Passwords do not match"}}
        # In hackathon mode, we use the email from the token (simplified)
        success = auth_service.reset_password(db, request.token, request.new_password)
        if success:
            return {"success": True, "data": {"message": "Password reset successfully"}, "error": None}
        return {"success": False, "data": None, "error": {"code": "RESET_FAILED", "message": "Failed to reset password"}}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "RESET_PASSWORD_FAILED", "message": str(e)}}

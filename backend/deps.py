from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import database
import models
from oauth2 import decode_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(database.get_db),
) -> models.User:
    """Dependency: Extract and validate the current user from the JWT token."""
    token = credentials.credentials
    payload = decode_token(token)

    user_id = payload.get("user_id")
    user_type = payload.get("type")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    if user_type == "doctor":
        user = db.query(models.Doctor).filter(models.Doctor.id == user_id).first()
    else:
        user = db.query(models.User).filter(models.User.userId == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def require_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(database.get_db),
) -> models.User:
    """Dependency: Verify the current user is an admin."""
    token = credentials.credentials
    payload = decode_token(token)

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    admin = db.query(models.User).filter(models.User.userId == user_id).first()
    if not admin or admin.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return admin

def require_doctor(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(database.get_db),
) -> models.Doctor:
    """Dependency: Verify the current user is a doctor."""
    token = credentials.credentials
    payload = decode_token(token)

    user_id = payload.get("user_id")
    user_type = payload.get("type")

    if not user_id or user_type != "doctor":
        raise HTTPException(status_code=403, detail="Doctor access required")

    doctor = db.query(models.Doctor).filter(models.Doctor.id == user_id).first()
    if not doctor:
        raise HTTPException(status_code=403, detail="Doctor not found")

    return doctor

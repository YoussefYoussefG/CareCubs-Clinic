from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

import database
import models
import oauth2
import schemas
import utils

router = APIRouter(tags=["authentication"])

@router.post(
    "/login",
    description="This route is for user or doctor login",
    response_model=list[schemas.LoginResponse],
)
async def user_login(
    login_info: schemas.UserLogin, db: Session = Depends(database.get_db)
):
    # Try finding doctor by username or email
    doctor = db.query(models.Doctor).filter(
        or_(
            models.Doctor.userName == login_info.username,
            models.Doctor.email == login_info.username,
        )
    ).first()

    if doctor:
        if not utils.verify_password(login_info.password, doctor.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
            )
        access_token = oauth2.create_access_token(
            data={"user_id": doctor.id, "type": "doctor"}
        )
        return [{"accessToken": access_token, "role": doctor.role, "userId": doctor.id}]

    # Try finding user by username or email
    user = db.query(models.User).filter(
        or_(
            models.User.userName == login_info.username,
            models.User.email == login_info.username,
        )
    ).first()

    if user:
        if not utils.verify_password(login_info.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
            )
        access_token = oauth2.create_access_token(
            data={"user_id": user.userId, "type": "user"}
        )
        return [{"accessToken": access_token, "role": user.role, "userId": user.userId}]

    # If neither found
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="User not found"
    )

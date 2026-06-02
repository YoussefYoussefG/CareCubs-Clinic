from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
import deps
import models
import schemas

router = APIRouter(tags=["notification"])


@router.post(
    "/add/fcmToken",
    status_code=status.HTTP_201_CREATED,
    description="Register an FCM token for push notifications.",
)
async def add_fcm_token(
    fcm_data: schemas.FCM,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    # Check if token already exists
    if db.query(models.FCMToken).filter(models.FCMToken.fcmToken == fcm_data.fcmToken).first():
        raise HTTPException(status_code=400, detail="FCM Token already exists")

    new_token = models.FCMToken(
        fcmToken=fcm_data.fcmToken,
        userId=fcm_data.userId,
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)

    return {"message": "FCM Token added successfully."}
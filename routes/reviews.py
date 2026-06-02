from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
import deps
import models
import schemas

router = APIRouter(tags=["reviews"])


# ─── Create ─────────────────────────────────────────────────────────────────

@router.post(
    "/add/review",
    status_code=status.HTTP_201_CREATED,
    description="Add a new review for a doctor.",
)
async def add_review(
    review: schemas.ReviewCreate,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    new_review = models.Review(
        parentId=review.parentId,
        doctorId=review.doctorId,
        review=review.review,
        rating=review.rating,
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return {"message": "Your review has been added successfully"}


# ─── Read ────────────────────────────────────────────────────────────────────

@router.get(
    "/get/review/{doctorId}",
    status_code=status.HTTP_200_OK,
    description="Get all reviews for a doctor (public).",
    response_model=List[schemas.ReviewResponse],
)
async def get_reviews(doctorId: int, db: Session = Depends(database.get_db)):
    reviews = db.query(models.Review).filter(models.Review.doctorId == doctorId).all()
    result = []
    for review in reviews:
        doctor = db.query(models.Doctor).filter(models.Doctor.id == review.doctorId).first()
        reviewer = db.query(models.User).filter(models.User.userId == review.parentId).first()
        doctor_name = f"Dr. {doctor.firstName} {doctor.lastName}" if doctor else "Unknown"
        reviewer_name = f"{reviewer.firstName} {reviewer.lastName}" if reviewer else "Unknown"
        result.append(schemas.ReviewResponse(
            reviewerName=reviewer_name,
            doctorName=doctor_name,
            review=review.review,
            rating=review.rating,
        ))
    return result


@router.get(
    "/get/reviews/barchart/{doctorId}",
    status_code=status.HTTP_200_OK,
    description="Get review bar chart data for a doctor.",
    response_model=List[schemas.BarChart],
)
async def get_reviews_barchart(
    doctorId: int,
    doctor: models.Doctor = Depends(deps.require_doctor),
    db: Session = Depends(database.get_db),
):
    result = []
    for stars in range(5, 0, -1):
        count = db.query(models.Review).filter(
            models.Review.doctorId == doctorId, models.Review.rating == stars
        ).count()
        result.append({"number": count, "stars": stars})
    return result


@router.get(
    "/get/reviews/barchart/{doctorId}/{adminId}",
    status_code=status.HTTP_200_OK,
    description="Get review bar chart data for a doctor (admin view).",
    response_model=List[schemas.BarChart],
)
async def get_reviews_barchart_admin(
    doctorId: int,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    result = []
    for stars in range(5, 0, -1):
        count = db.query(models.Review).filter(
            models.Review.doctorId == doctorId, models.Review.rating == stars
        ).count()
        result.append({"number": count, "stars": stars})
    return result


# ─── Analytics ───────────────────────────────────────────────────────────────

@router.get(
    "/get/doctor/avg/rating/{doctorId}",
    status_code=status.HTTP_200_OK,
    description="Get average rating for a doctor.",
    response_model=schemas.AvgRating,
)
async def get_avg_rating(
    doctorId: int,
    doctor: models.Doctor = Depends(deps.require_doctor),
    db: Session = Depends(database.get_db),
):
    reviews = db.query(models.Review).filter(models.Review.doctorId == doctorId).all()
    if not reviews:
        return {"avgRating": 0.0, "count": 0}

    total = sum(r.rating for r in reviews)
    avg = round(float(total / len(reviews)), 2)
    return {"avgRating": avg, "count": len(reviews)}


@router.get(
    "/get/doctor/avg/rating/{doctorId}/{adminId}",
    status_code=status.HTTP_200_OK,
    description="Get average rating for a doctor (admin view).",
    response_model=schemas.AvgRating,
)
async def get_avg_rating_admin(
    doctorId: int,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    reviews = db.query(models.Review).filter(models.Review.doctorId == doctorId).all()
    if not reviews:
        return {"avgRating": 0.0, "count": 0}

    total = sum(r.rating for r in reviews)
    avg = round(float(total / len(reviews)), 2)
    return {"avgRating": avg, "count": len(reviews)}
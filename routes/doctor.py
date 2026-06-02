import random

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
import deps
import models
import oauth2
import schemas
import utils

router = APIRouter(tags=["doctor"])


# ─── Create ─────────────────────────────────────────────────────────────────

@router.post(
    "/add/doctor/{adminId}",
    status_code=status.HTTP_201_CREATED,
    description="Create a new doctor (admin only).",
    response_model=schemas.LoginResponse,
)
async def create_doctor(
    user: schemas.AddDoctor,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    # Check for duplicate email
    existing = db.query(models.Doctor).filter(models.Doctor.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Doctor with the same email already exists",
        )

    if not utils.is_complex_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is not complex enough. It must be at least 8 characters long, contain uppercase, lowercase, digit, and special characters.",
        )

    hashed_password = utils.hash(user.password)

    # Generate unique username
    user_name = f"{user.firstName}{user.lastName}{random.randint(1, 10000)}"
    while db.query(models.Doctor).filter(models.Doctor.userName == user_name).first():
        user_name = f"{user.firstName}{user.lastName}{random.randint(1, 10000)}"

    new_doctor = models.Doctor(
        userName=user_name,
        email=user.email,
        password=hashed_password,
        firstName=user.firstName,
        lastName=user.lastName,
        price=user.price,
        role="doctor",
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    access_token = oauth2.create_access_token(
        data={"user_id": new_doctor.id, "type": "doctor"}
    )
    return {"accessToken": access_token, "role": new_doctor.role, "userId": new_doctor.id}


# ─── Read ────────────────────────────────────────────────────────────────────

@router.get(
    "/get/doctor/{doctorId}/{userId}",
    description="Get doctor data by doctorId (authenticated).",
)
async def get_doctor_by_id(
    doctorId: int,
    userId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctorId).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return {
        "doctor": {
            "doctorId": doctor.id,
            "firstName": doctor.firstName,
            "lastName": doctor.lastName,
            "email": doctor.email,
            "userName": doctor.userName,
            "createdAt": str(doctor.createdAt),
            "profilePicture": doctor.profilePicture,
            "role": doctor.role,
            "rating": doctor.rating,
            "numberOfRating": doctor.numberOfRating,
            "price": doctor.price,
        }
    }


@router.get(
    "/doctorList",
    description="Fetch all doctors (public).",
    response_model=list[schemas.DoctorList],
)
async def doctor_list(db: Session = Depends(database.get_db)):
    doctors = db.query(models.Doctor).all()
    if not doctors:
        raise HTTPException(status_code=404, detail="No doctors found")

    doctors_data = []
    for doctor in doctors:
        title = f"Dr. {doctor.firstName} {doctor.lastName}"
        reviews = db.query(models.Review).filter(models.Review.doctorId == doctor.id).all()
        num_reviews = len(reviews)
        total_rating = sum(r.rating for r in reviews)
        avg_rating = round(total_rating / num_reviews, 2) if num_reviews > 0 else 0

        doctors_data.append({
            "title": title,
            "link": "/Signup",
            "thumbnail": doctor.profilePicture,
            "id": doctor.id,
            "numberOfReviews": num_reviews,
            "avarageRating": avg_rating,
        })

    return doctors_data


@router.get(
    "/get/all/doctors/{adminId}",
    description="Get all doctors (admin only).",
)
async def get_all_doctors(
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    doctors = db.query(models.Doctor).all()
    return [
        {
            "id": d.id,
            "firstName": d.firstName,
            "lastName": d.lastName,
            "email": d.email,
            "userName": d.userName,
            "createdAt": str(d.createdAt),
            "profilePicture": d.profilePicture,
            "price": d.price,
        }
        for d in doctors
    ]


@router.get(
    "/get/doctor/{doctorId}",
    description="Get own doctor profile (doctor only).",
)
async def get_own_doctor_profile(
    doctorId: int,
    doctor: models.Doctor = Depends(deps.require_doctor),
    db: Session = Depends(database.get_db),
):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctorId).first()
    if not db_doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")

    return {
        "doctorId": db_doctor.id,
        "firstName": db_doctor.firstName,
        "lastName": db_doctor.lastName,
        "email": db_doctor.email,
        "userName": db_doctor.userName,
        "createdAt": str(db_doctor.createdAt),
        "profilePicture": db_doctor.profilePicture,
        "role": db_doctor.role,
        "rating": db_doctor.rating,
        "numberOfRating": db_doctor.numberOfRating,
        "price": db_doctor.price,
    }


@router.get(
    "/get/doctor/{doctorId}/{adminId}",
    description="Get doctor profile by admin.",
)
async def get_doctor_by_admin(
    doctorId: int,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctorId).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")

    return {
        "doctorId": doctor.id,
        "firstName": doctor.firstName,
        "lastName": doctor.lastName,
        "email": doctor.email,
        "userName": doctor.userName,
        "createdAt": str(doctor.createdAt),
        "profilePicture": doctor.profilePicture,
        "role": doctor.role,
        "rating": doctor.rating,
        "numberOfRating": doctor.numberOfRating,
        "price": doctor.price,
    }


# ─── Analytics ───────────────────────────────────────────────────────────────

@router.get(
    "/get/doctors/total/price/{adminId}",
    description="Get total revenue from all appointments (admin only).",
)
async def get_doctors_total_price(
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    appointments = db.query(models.Appointment).all()
    total_price = 0
    for appointment in appointments:
        doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctorId).first()
        if doctor:
            total_price += doctor.price
    return {"totalPrice": total_price}


@router.get(
    "/get/Number/of/doctors/{adminId}",
    description="Get total number of doctors (admin only).",
)
async def get_number_of_doctors(
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    count = db.query(models.Doctor).count()
    return {"totalNumberOfDoctors": count}


# ─── Update ──────────────────────────────────────────────────────────────────

@router.put(
    "/update/doctor/{doctorId}",
    description="Update own doctor profile.",
    response_model=schemas.Doctor,
)
async def update_doctor(
    doctor: schemas.UpdateDoctor,
    doctorId: int,
    current_doctor: models.Doctor = Depends(deps.require_doctor),
    db: Session = Depends(database.get_db),
):
    # Check username uniqueness
    if db.query(models.Doctor).filter(
        models.Doctor.userName == doctor.userName, models.Doctor.id != doctorId
    ).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Check email uniqueness
    if db.query(models.Doctor).filter(
        models.Doctor.email == doctor.email, models.Doctor.id != doctorId
    ).first():
        raise HTTPException(status_code=400, detail="Email already taken")

    existing = db.query(models.Doctor).filter(models.Doctor.id == doctorId).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Doctor not found")

    hashed_password = existing.password if doctor.password == "" else utils.hash(doctor.password)

    db.query(models.Doctor).filter(models.Doctor.id == doctorId).update({
        "userName": doctor.userName,
        "email": doctor.email,
        "password": hashed_password,
        "firstName": doctor.firstName,
        "lastName": doctor.lastName,
        "profilePicture": doctor.profilePic,
        "price": doctor.price,
    })
    db.commit()

    updated = db.query(models.Doctor).filter(models.Doctor.id == doctorId).first()
    return {
        "doctorId": updated.id,
        "firstName": updated.firstName,
        "lastName": updated.lastName,
        "email": updated.email,
        "userName": updated.userName,
        "createdAt": str(updated.createdAt),
        "profilePicture": updated.profilePicture,
        "role": updated.role,
        "rating": updated.rating,
        "numberOfRating": updated.numberOfRating,
        "price": updated.price,
    }


@router.put(
    "/update/doctor/admin/{adminId}",
    description="Update doctor profile (admin only).",
)
async def update_doctor_by_admin(
    doctor: schemas.UpdateDoctorAdmin,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    # Check username uniqueness
    if db.query(models.Doctor).filter(
        models.Doctor.userName == doctor.userName, models.Doctor.id != doctor.doctorId
    ).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Check email uniqueness
    if db.query(models.Doctor).filter(
        models.Doctor.email == doctor.email, models.Doctor.id != doctor.doctorId
    ).first():
        raise HTTPException(status_code=400, detail="Email already taken")

    existing = db.query(models.Doctor).filter(models.Doctor.id == doctor.doctorId).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Doctor not found")

    hashed_password = existing.password if doctor.password == "" else utils.hash(doctor.password)

    db.query(models.Doctor).filter(models.Doctor.id == doctor.doctorId).update({
        "userName": doctor.userName,
        "email": doctor.email,
        "password": hashed_password,
        "firstName": doctor.firstName,
        "lastName": doctor.lastName,
        "profilePicture": doctor.profilePic,
        "price": doctor.price,
    })
    db.commit()

    updated = db.query(models.Doctor).filter(models.Doctor.id == doctor.doctorId).first()
    return {
        "doctorId": updated.id,
        "firstName": updated.firstName,
        "lastName": updated.lastName,
        "email": updated.email,
        "userName": updated.userName,
        "createdAt": str(updated.createdAt),
        "profilePicture": updated.profilePicture,
        "price": updated.price,
    }


# ─── Delete ──────────────────────────────────────────────────────────────────

@router.delete(
    "/delete/doctor/{doctorId}/{adminId}",
    description="Delete a doctor (admin only).",
)
async def delete_doctor(
    doctorId: int,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctorId).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")

    # Delete associated appointments first
    db.query(models.Appointment).filter(models.Appointment.doctorId == doctorId).delete()
    db.delete(doctor)
    db.commit()

    return {"message": "Doctor deleted successfully"}

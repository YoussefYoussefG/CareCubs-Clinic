from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
import deps
import models
import oauth2
import schemas
import utils

router = APIRouter(tags=["user"])


# ─── Create ─────────────────────────────────────────────────────────────────

@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    description="Create a new user (customer).",
    response_model=schemas.LoginResponse,
)
async def signup(
    user: schemas.UserSignup, db: Session = Depends(database.get_db)
):
    existing = db.query(models.User).filter(
        (models.User.userName == user.userName) | (models.User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same username or email already exists",
        )

    if not utils.is_complex_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is not complex enough. It must be at least 8 characters long, contain uppercase, lowercase, digit, and special characters.",
        )

    hashed_password = utils.hash(user.password)
    new_user = models.User(
        userName=user.userName,
        email=user.email,
        password=hashed_password,
        firstName=user.firstName,
        lastName=user.lastName,
        PhoneNumber=user.phone,
        role="customer",
        profilePicture="https://i.imgur.com/9g7aq8u.png",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = oauth2.create_access_token(
        data={"user_id": new_user.userId, "type": "user"}
    )
    return {"accessToken": access_token, "role": new_user.role, "userId": new_user.userId}


@router.post(
    "/add/user/{adminId}",
    status_code=status.HTTP_201_CREATED,
    description="Create a new user with any role (admin only).",
    response_model=schemas.LoginResponse,
)
async def add_user(
    user: schemas.AddUser,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    existing = db.query(models.User).filter(
        (models.User.userName == user.userName) | (models.User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same username or email already exists",
        )

    if not utils.is_complex_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is not complex enough. It must be at least 8 characters long, contain uppercase, lowercase, digit, and special characters.",
        )

    hashed_password = utils.hash(user.password)
    new_user = models.User(
        userName=user.userName,
        email=user.email,
        password=hashed_password,
        firstName=user.firstName,
        lastName=user.lastName,
        PhoneNumber=user.phone,
        role=user.role,
        profilePicture="https://i.imgur.com/9g7aq8u.png",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = oauth2.create_access_token(
        data={"user_id": new_user.userId, "type": "user"}
    )
    return {"accessToken": access_token, "role": new_user.role, "userId": new_user.userId}


# ─── Read ────────────────────────────────────────────────────────────────────

def _user_to_dict(user):
    """Helper to convert User model to response dict."""
    return {
        "userId": user.userId,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "userName": user.userName,
        "createdAt": str(user.createdAt),
        "phone": user.PhoneNumber,
        "age": user.age,
        "profilePicture": user.profilePicture,
        "role": user.role,
    }


@router.get(
    "/get/user/{userId}",
    description="Get own user profile.",
    response_model=schemas.User,
)
async def get_own_profile(
    userId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.userId == userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_to_dict(user)


@router.get(
    "/get/user/{userId}/{adminId}",
    description="Get user profile by admin.",
    response_model=schemas.User,
)
async def get_user_by_admin(
    userId: int,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.userId == userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_to_dict(user)


@router.get(
    "/get/all/users/{adminId}",
    description="Get all users (admin only).",
)
async def get_all_users(
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    users = db.query(models.User).all()
    return [
        {
            "id": u.userId,
            "userName": u.userName,
            "email": u.email,
            "firstName": u.firstName,
            "lastName": u.lastName,
            "createdAt": str(u.createdAt),
            "phone": u.PhoneNumber,
            "age": u.age,
            "profilePicture": u.profilePicture,
            "role": u.role,
        }
        for u in users
    ]


# ─── Analytics ───────────────────────────────────────────────────────────────

@router.get(
    "/get/Number/of/users/{adminId}",
    description="Get user count by role (admin only).",
)
async def get_user_counts(
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    users = db.query(models.User).all()
    customers = sum(1 for u in users if u.role == "customer")
    admins = sum(1 for u in users if u.role == "admin")
    staff = sum(1 for u in users if u.role == "staff")
    return {
        "totalNumberOfCustomers": customers,
        "totalNumberOfAdmins": admins,
        "totalNumberOfStaff": staff,
    }


# ─── Update ──────────────────────────────────────────────────────────────────

@router.put(
    "/update/user/{userId}",
    description="Update own user profile.",
    response_model=schemas.User,
)
async def update_user(
    user: schemas.UpdateUser,
    userId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    # Check username uniqueness
    if db.query(models.User).filter(
        models.User.userName == user.userName, models.User.userId != userId
    ).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Check email uniqueness
    if db.query(models.User).filter(
        models.User.email == user.email, models.User.userId != userId
    ).first():
        raise HTTPException(status_code=400, detail="Email already taken")

    existing = db.query(models.User).filter(models.User.userId == userId).first()
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = existing.password if user.password == "" else utils.hash(user.password)

    db.query(models.User).filter(models.User.userId == userId).update({
        "userName": user.userName,
        "email": user.email,
        "password": hashed_password,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "profilePicture": user.profilePicture,
        "PhoneNumber": user.phoneNumber,
        "age": user.age,
    })
    db.commit()

    updated = db.query(models.User).filter(models.User.userId == userId).first()
    return _user_to_dict(updated)


@router.put(
    "/update/user/admin/{adminId}",
    description="Update any user's profile (admin only).",
    response_model=schemas.User,
)
async def update_user_by_admin(
    user: schemas.UpdateUserAdmin,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    # Check username uniqueness
    if db.query(models.User).filter(
        models.User.userName == user.userName, models.User.userId != user.userId
    ).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Check email uniqueness
    if db.query(models.User).filter(
        models.User.email == user.email, models.User.userId != user.userId
    ).first():
        raise HTTPException(status_code=400, detail="Email already taken")

    existing = db.query(models.User).filter(models.User.userId == user.userId).first()
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = existing.password if user.password == "" else utils.hash(user.password)

    db.query(models.User).filter(models.User.userId == user.userId).update({
        "userName": user.userName,
        "email": user.email,
        "password": hashed_password,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "profilePicture": user.profilePicture,
        "PhoneNumber": user.phoneNumber,
        "age": user.age,
        "role": user.role,
    })
    db.commit()

    updated = db.query(models.User).filter(models.User.userId == user.userId).first()
    return _user_to_dict(updated)


# ─── Delete ──────────────────────────────────────────────────────────────────

@router.delete(
    "/delete/user/{userId}/{adminId}",
    description="Delete a user and all related records (admin only).",
)
async def delete_user(
    userId: int,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.userId == userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Clean up related data
    db.query(models.Appointment).filter(models.Appointment.parentId == userId).delete()
    db.query(models.Patient).filter(models.Patient.parentId == userId).delete()

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
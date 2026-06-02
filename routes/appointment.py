from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
import deps
import models
import oauth2
import schemas

router = APIRouter(tags=["Appointment"])


# ─── Create ─────────────────────────────────────────────────────────────────

@router.post(
    "/add/appointment",
    status_code=status.HTTP_201_CREATED,
    description="Add a new appointment (parent user).",
)
async def add_appointment(
    appointment: schemas.AddAppointment,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    # Check for duplicate appointment at the same time
    existing = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.appointmentDate == appointment.appointmentDate,
            models.Appointment.fromTime == appointment.From,
            models.Appointment.toTime == appointment.To,
        )
        .first()
    )
    if existing:
        return {"message": "Appointment already exists"}

    new_appointment = models.Appointment(
        parentId=appointment.parentId,
        doctorId=appointment.doctorId,
        patientId=appointment.patientId,
        appointmentDate=appointment.appointmentDate,
        fromTime=appointment.From,
        toTime=appointment.To,
        isTaken=appointment.isTaken,
        Paid=False,
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    # Grant MR access if not already present
    if not db.query(models.MRAccess).filter(
        models.MRAccess.patientId == appointment.patientId,
        models.MRAccess.doctorId == appointment.doctorId,
    ).first():
        mra = models.MRAccess(patientId=appointment.patientId, doctorId=appointment.doctorId)
        db.add(mra)
        db.commit()

    return {"message": "Appointment added successfully"}


@router.post(
    "/add/appointment/{adminId}",
    status_code=status.HTTP_201_CREATED,
    description="Add a new appointment (admin).",
)
async def add_appointment_admin(
    appointment: schemas.AddAppointment,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    existing = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.appointmentDate == appointment.appointmentDate,
            models.Appointment.fromTime == appointment.From,
            models.Appointment.toTime == appointment.To,
        )
        .first()
    )
    if existing:
        return {"message": "Appointment already exists"}

    new_appointment = models.Appointment(
        parentId=appointment.parentId,
        doctorId=appointment.doctorId,
        patientId=appointment.patientId,
        appointmentDate=appointment.appointmentDate,
        fromTime=appointment.From,
        toTime=appointment.To,
        isTaken=appointment.isTaken,
        Paid=False,
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    # Grant MR access if not already present
    if not db.query(models.MRAccess).filter(
        models.MRAccess.patientId == appointment.patientId,
        models.MRAccess.doctorId == appointment.doctorId,
    ).first():
        mra = models.MRAccess(patientId=appointment.patientId, doctorId=appointment.doctorId)
        db.add(mra)
        db.commit()

    return {"message": "Appointment added successfully"}


# ─── Read ────────────────────────────────────────────────────────────────────

def _build_appointment_data(appointment, db, include_doctor_info=True, include_parent_pic=True):
    """Helper to build appointment response dict."""
    user = db.query(models.User).filter(models.User.userId == appointment.parentId).first()
    patient = db.query(models.Patient).filter(models.Patient.id == appointment.patientId).first()
    doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctorId).first()

    data = {
        "appointmentId": appointment.id,
        "parentId": user.userId if user else None,
        "patientId": patient.id if patient else None,
        "doctorId": doctor.id if doctor else None,
        "patientFirstName": patient.firstName if patient else None,
        "parentFirstName": user.firstName if user else None,
        "parentLastName": user.lastName if user else None,
        "appointmentDate": appointment.appointmentDate,
        "From": appointment.fromTime,
        "To": appointment.toTime,
        "isTaken": appointment.isTaken,
        "Paid": appointment.Paid,
    }

    if include_doctor_info and doctor:
        data["doctorFirstName"] = doctor.firstName
        data["doctorLastName"] = doctor.lastName
        data["doctorPic"] = doctor.profilePicture

    if include_parent_pic and user:
        data["parentPic"] = user.profilePicture

    return data


@router.get(
    "/get/appointment/{parentId}",
    status_code=status.HTTP_200_OK,
    description="Get all appointments for a parent.",
)
async def get_parent_appointments(
    parentId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    appointments = db.query(models.Appointment).filter(
        models.Appointment.parentId == parentId
    ).all()

    result = []
    for appt in appointments:
        user = db.query(models.User).filter(models.User.userId == appt.parentId).first()
        patient = db.query(models.Patient).filter(models.Patient.id == appt.patientId).first()
        doctor = db.query(models.Doctor).filter(models.Doctor.id == appt.doctorId).first()

        result.append({
            "id": appt.id,
            "parentId": user.userId if user else None,
            "patientId": patient.id if patient else None,
            "doctorId": appt.doctorId,
            "patientFirstName": patient.firstName if patient else None,
            "parentFirstName": user.firstName if user else None,
            "parentLastName": user.lastName if user else None,
            "parentPic": user.profilePicture if user else None,
            "doctorPic": doctor.profilePicture if doctor else None,
            "doctorFirstName": doctor.firstName if doctor else None,
            "doctorLastName": doctor.lastName if doctor else None,
            "appointmentDate": appt.appointmentDate,
            "From": appt.fromTime,
            "To": appt.toTime,
            "isTaken": appt.isTaken,
            "Paid": appt.Paid,
        })
    return result


@router.get(
    "/get/doctor/appointments/table/{doctorId}/{userId}",
    status_code=status.HTTP_200_OK,
    description="Get all appointments for a specific doctor (table view).",
)
async def get_doctor_appointments_table(
    doctorId: int,
    userId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    appointments = db.query(models.Appointment).filter(
        models.Appointment.doctorId == doctorId
    ).all()

    result = []
    for appt in appointments:
        user = db.query(models.User).filter(models.User.userId == appt.parentId).first()
        patient = db.query(models.Patient).filter(models.Patient.id == appt.patientId).first()

        result.append({
            "appointmentId": appt.id,
            "parentId": user.userId if user else None,
            "patientId": patient.id if patient else None,
            "patientFirstName": patient.firstName if patient else None,
            "parentFirstName": user.firstName if user else None,
            "parentLastName": user.lastName if user else None,
            "parentPic": user.profilePicture if user else None,
            "appointmentDate": appt.appointmentDate,
            "From": appt.fromTime,
            "To": appt.toTime,
            "isTaken": appt.isTaken,
            "Paid": appt.Paid,
        })
    return result


@router.get(
    "/get/all/appointments",
    description="Get all appointments (public).",
)
async def get_all_appointments_public(db: Session = Depends(database.get_db)):
    appointments = db.query(models.Appointment).all()
    return [_build_appointment_data(appt, db) for appt in appointments]


@router.get(
    "/get/all/appointments/{adminId}",
    description="Get all appointments (admin).",
)
async def get_all_appointments_admin(
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    appointments = db.query(models.Appointment).all()
    result = []
    for appt in appointments:
        user = db.query(models.User).filter(models.User.userId == appt.parentId).first()
        patient = db.query(models.Patient).filter(models.Patient.id == appt.patientId).first()
        doctor = db.query(models.Doctor).filter(models.Doctor.id == appt.doctorId).first()

        result.append({
            "id": appt.id,
            "patientFirstName": patient.firstName if patient else None,
            "parentFirstName": user.firstName if user else None,
            "parentLastName": user.lastName if user else None,
            "doctorFirstName": doctor.firstName if doctor else None,
            "doctorLastName": doctor.lastName if doctor else None,
            "doctorId": doctor.id if doctor else None,
            "appointmentDate": appt.appointmentDate,
            "From": appt.fromTime,
            "To": appt.toTime,
            "Paid": appt.Paid,
        })
    return result


@router.get(
    "/get/all/appointments/table/{adminId}",
    status_code=status.HTTP_200_OK,
    description="Get all appointments table view (admin).",
)
async def get_all_appointments_table(
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    appointments = db.query(models.Appointment).all()
    return [_build_appointment_data(appt, db) for appt in appointments]


@router.get(
    "/get/appointment/{appointmentId}/{adminId}",
    description="Get a single appointment by ID (admin).",
)
async def get_appointment_by_id(
    appointmentId: int,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointmentId
    ).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    user = db.query(models.User).filter(models.User.userId == appointment.parentId).first()
    patient = db.query(models.Patient).filter(models.Patient.id == appointment.patientId).first()
    doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctorId).first()

    return {
        "id": appointment.id,
        "patientFirstName": patient.firstName if patient else None,
        "parentFirstName": user.firstName if user else None,
        "parentLastName": user.lastName if user else None,
        "doctorFirstName": doctor.firstName if doctor else None,
        "doctorLastName": doctor.lastName if doctor else None,
        "doctorId": doctor.id if doctor else None,
        "appointmentDate": appointment.appointmentDate,
        "From": appointment.fromTime,
        "To": appointment.toTime,
        "Paid": appointment.Paid,
    }


@router.get(
    "/get/all/appointments/{staffId}",
    description="Get all appointments (staff).",
)
async def get_all_appointments_staff(
    staffId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    appointments = db.query(models.Appointment).all()
    return [_build_appointment_data(appt, db) for appt in appointments]


# ─── Update ──────────────────────────────────────────────────────────────────

@router.put(
    "/update/appointments/{adminId}/{appointmentId}",
    description="Update an appointment (admin).",
)
async def update_appointment(
    adminId: int,
    appointmentId: int,
    appointment: schemas.UpdateAppointment,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    appt_query = db.query(models.Appointment).filter(
        models.Appointment.id == appointmentId
    )
    existing = appt_query.first()
    if not existing:
        raise HTTPException(status_code=404, detail="Appointment not found")

    update_data = {
        "doctorId": appointment.doctorId if appointment.doctorId is not None else existing.doctorId,
        "appointmentDate": appointment.appointmentDate if appointment.appointmentDate is not None else existing.appointmentDate,
        "fromTime": appointment.From if appointment.From is not None else existing.fromTime,
        "toTime": appointment.To if appointment.To is not None else existing.toTime,
        "isTaken": True,
    }
    appt_query.update(update_data)
    db.commit()

    return appt_query.first()


# ─── Delete ──────────────────────────────────────────────────────────────────

@router.delete(
    "/delete/appointment/{appointmentId}/{adminId}",
    status_code=status.HTTP_200_OK,
    description="Delete an appointment (admin).",
)
async def delete_appointment(
    appointmentId: int,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointmentId
    ).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found.")

    # Store IDs before deletion
    patient_id = appointment.patientId
    doctor_id = appointment.doctorId

    mra = db.query(models.MRAccess).filter(
        models.MRAccess.patientId == patient_id,
        models.MRAccess.doctorId == doctor_id,
    ).first()

    db.delete(appointment)
    db.commit()

    # Remove MR access if no more appointments between this patient and doctor
    remaining = db.query(models.Appointment).filter(
        models.Appointment.patientId == patient_id,
        models.Appointment.doctorId == doctor_id,
    ).first()
    if not remaining and mra:
        db.delete(mra)
        db.commit()

    return {"message": "Appointment deleted successfully"}

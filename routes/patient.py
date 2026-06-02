from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import database
import deps
import models
import oauth2
import schemas

router = APIRouter(tags=["patient"])


# ─── Create ─────────────────────────────────────────────────────────────────

@router.post(
    "/add/patient",
    status_code=status.HTTP_201_CREATED,
    description="Add a new patient (parent user).",
    response_model=schemas.PatientResponse,
)
async def create_patient(
    user: schemas.AddPatient,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    parent_user = db.query(models.User).filter(models.User.userId == user.parentId).first()
    if not parent_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user.parentId} not found.",
        )

    new_patient = models.Patient(
        firstName=user.firstName,
        lastName=user.lastName,
        parentFirstName=parent_user.firstName,
        parentLastName=parent_user.lastName,
        parentPhoneNumber=parent_user.PhoneNumber,
        parentId=user.parentId,
        age=user.age,
        gender=user.gender,
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    # Auto-create medical record for the patient
    new_medical_record = models.MedicalRecord(patientId=new_patient.id)
    try:
        db.add(new_medical_record)
        db.commit()
        db.refresh(new_medical_record)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating medical record: {e}")

    return new_patient


@router.post(
    "/add/patient/{adminId}",
    status_code=status.HTTP_201_CREATED,
    description="Add a new patient (admin).",
    response_model=schemas.PatientResponse,
)
async def create_patient_admin(
    user: schemas.AddPatient,
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    parent_user = db.query(models.User).filter(models.User.userId == user.parentId).first()
    if not parent_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user.parentId} not found.",
        )

    new_patient = models.Patient(
        firstName=user.firstName,
        lastName=user.lastName,
        parentFirstName=parent_user.firstName,
        parentLastName=parent_user.lastName,
        parentPhoneNumber=parent_user.PhoneNumber,
        parentId=user.parentId,
        age=user.age,
        gender=user.gender,
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    new_medical_record = models.MedicalRecord(patientId=new_patient.id)
    try:
        db.add(new_medical_record)
        db.commit()
        db.refresh(new_medical_record)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating medical record: {e}")

    return new_patient


# ─── Read ────────────────────────────────────────────────────────────────────

@router.get(
    "/get/patients/{parentId}",
    description="Get all patients for a parent.",
    response_model=list[schemas.PatientResponse],
)
async def get_patients_by_parent(
    parentId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    patients = db.query(models.Patient).filter(models.Patient.parentId == parentId).all()
    return patients


@router.get(
    "/get/patient/{patientId}/{parentId}",
    description="Get a specific patient by ID (parent auth).",
    response_model=schemas.PatientResponse,
)
async def get_patient_by_id(
    patientId: int,
    parentId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    patient = db.query(models.Patient).filter(models.Patient.id == patientId).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.get(
    "/patientList/{doctorId}",
    description="Get all patients for a specific doctor.",
    response_model=list[schemas.PatientListItem],
)
async def list_patients_for_doctor(
    doctorId: int,
    doctor: models.Doctor = Depends(deps.require_doctor),
    db: Session = Depends(database.get_db),
):
    access_records = db.query(models.MRAccess).filter(models.MRAccess.doctorId == doctorId).all()
    patients = []

    for record in access_records:
        patient_list = db.query(models.Patient).filter(models.Patient.id == record.patientId).all()
        for patient in patient_list:
            parent = db.query(models.User).filter(models.User.userId == patient.parentId).first()
            pic = parent.profilePicture if parent and parent.profilePicture else "None"
            patients.append({
                "parentPic": pic,
                "patientFirstName": patient.firstName,
                "patientLastName": patient.lastName,
                "parentFirstName": parent.firstName if parent else "",
                "parentLastName": parent.lastName if parent else "",
                "patientId": patient.id,
            })

    return patients


@router.get(
    "/patient/{patientId}/{doctorId}",
    description="Get patient info (doctor view).",
    response_model=schemas.ReturnPatient,
)
async def get_patient_info_doctor(
    patientId: int,
    doctorId: int,
    doctor: models.Doctor = Depends(deps.require_doctor),
    db: Session = Depends(database.get_db),
):
    patient = db.query(models.Patient).filter(models.Patient.id == patientId).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    parent = db.query(models.User).filter(models.User.userId == patient.parentId).first()
    pic = parent.profilePicture if parent and parent.profilePicture else "None"

    return {
        "firstName": patient.firstName,
        "lastName": patient.lastName,
        "parentFirstName": parent.firstName if parent else "",
        "parentLastName": parent.lastName if parent else "",
        "parentPic": pic,
        "age": patient.age,
        "id": patientId,
    }


@router.get(
    "/get/all/patients/{adminId}",
    description="Get all patients (admin only).",
    response_model=list[schemas.PatientResponse],
)
async def get_all_patients(
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    return db.query(models.Patient).all()


@router.get(
    "/get/all/patientsObj/{adminId}",
    description="Get all patients with parent info (admin only).",
)
async def get_all_patients_obj(
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    patients = db.query(models.Patient).all()
    result = []
    for patient in patients:
        parent = db.query(models.User).filter(models.User.userId == patient.parentId).first()
        pic = parent.profilePicture if parent and parent.profilePicture else "https://i.imgur.com/9g7aq8u.png"
        result.append({
            "parentPic": pic,
            "patientFirstName": patient.firstName,
            "patientLastName": patient.lastName,
            "parentFirstName": parent.firstName if parent else "",
            "parentLastName": parent.lastName if parent else "",
            "patientId": patient.id,
        })
    return result


# ─── Analytics ───────────────────────────────────────────────────────────────

@router.get(
    "/get/Number/of/patients/{adminId}",
    description="Get total number of patients (admin only).",
)
async def get_number_of_patients(
    adminId: int,
    admin: models.User = Depends(deps.require_admin),
    db: Session = Depends(database.get_db),
):
    count = db.query(models.Patient).count()
    return {"totalNumberOfPatients": count}


# ─── Update ──────────────────────────────────────────────────────────────────

@router.put(
    "/update/patient/{patientId}/{parentId}",
    description="Update patient info.",
    response_model=schemas.Patient,
)
async def update_patient(
    patient: schemas.UpdatePatient,
    patientId: int,
    parentId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    patient_query = db.query(models.Patient).filter(models.Patient.id == patientId)
    if not patient_query.first():
        raise HTTPException(status_code=404, detail="Patient not found")

    patient_query.update({
        "age": patient.age,
        "firstName": patient.firstName,
        "lastName": patient.lastName,
        "gender": patient.gender,
    })
    db.commit()

    return db.query(models.Patient).filter(models.Patient.id == patientId).first()


# ─── Delete ──────────────────────────────────────────────────────────────────

@router.delete(
    "/delete/patient/{patientId}/{userId}",
    description="Delete a patient and all related records.",
)
async def delete_patient(
    patientId: int,
    userId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    patient = db.query(models.Patient).filter(models.Patient.id == patientId).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")

    # Delete related records in order
    db.query(models.MRAccess).filter(models.MRAccess.patientId == patientId).delete()
    db.query(models.Appointment).filter(models.Appointment.patientId == patientId).delete()

    medical_record = db.query(models.MedicalRecord).filter(
        models.MedicalRecord.patientId == patientId
    ).first()
    if medical_record:
        db.delete(medical_record)

    db.delete(patient)
    db.commit()

    return {"message": "Patient deleted successfully"}

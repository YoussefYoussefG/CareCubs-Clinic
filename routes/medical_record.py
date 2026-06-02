from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
import deps
import models
import schemas

router = APIRouter(tags=["Medical Record"])


# ─── Read ────────────────────────────────────────────────────────────────────

@router.get(
    "/get/medicalRecord/{parentId}/{patientId}",
    description="Get all medical records for a patient (parent view).",
    response_model=list[schemas.MedicalRecordResponse],
)
async def get_medical_record_parent(
    patientId: int,
    parentId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    records = db.query(models.MedicalRecord).filter(
        models.MedicalRecord.patientId == patientId
    ).all()
    for record in records:
        record.createdAt = record.createdAt.isoformat()
    return records


@router.get(
    "/getMedicalRecord/{doctorId}/{patientId}",
    description="Get all medical records for a patient (doctor view).",
    response_model=list[schemas.MedicalRecordResponse],
)
async def get_medical_record_doctor(
    doctorId: int,
    patientId: int,
    doctor: models.Doctor = Depends(deps.require_doctor),
    db: Session = Depends(database.get_db),
):
    records = db.query(models.MedicalRecord).filter(
        models.MedicalRecord.patientId == patientId
    ).all()
    for record in records:
        record.createdAt = record.createdAt.isoformat()
    return records


# ─── Update (full) ──────────────────────────────────────────────────────────

@router.put(
    "/update/medicalRecord/{patientId}/{doctorId}",
    description="Update all medical record fields for a patient.",
)
async def update_medical_record(
    record: schemas.UpdateMedicalRecord,
    patientId: int,
    doctorId: int,
    doctor: models.Doctor = Depends(deps.require_doctor),
    db: Session = Depends(database.get_db),
):
    mr_query = db.query(models.MedicalRecord).filter(
        models.MedicalRecord.patientId == patientId
    )
    if not mr_query.first():
        raise HTTPException(status_code=404, detail="Medical record not found")

    mr_query.update({
        "notes": record.notes,
        "treatment": record.treatment,
        "healthCondition": record.healthCondition,
        "vaccine": record.vaccine,
        "allergies": record.allergies,
        "pastConditions": record.pastConditions,
        "chronicConditions": record.chronicConditions,
        "surgicalHistory": record.surgicalHistory,
        "medications": record.medications,
        "radiologyReport": record.radiologyReport,
    })
    db.commit()

    return {"message": "Medical Record updated successfully"}


# ─── Update (individual fields) ─────────────────────────────────────────────

@router.put(
    "/update/medicalRecord/radiologyReport/{userId}/{medicalRecordId}",
    description="Update radiology report.",
)
async def update_radiology_report(
    radiology_report: schemas.RadiologyReportUpdate,
    userId: int,
    medicalRecordId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    db.query(models.MedicalRecord).filter(
        models.MedicalRecord.id == medicalRecordId
    ).update({"radiologyReport": radiology_report.radiologyReport})
    db.commit()
    return {"message": "Medical Record (radiologyReport) updated successfully"}


@router.put(
    "/update/medicalRecord/medications/{userId}/{medicalRecordId}",
    description="Update medications.",
)
async def update_medications(
    medications: schemas.MedicationsUpdate,
    userId: int,
    medicalRecordId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    db.query(models.MedicalRecord).filter(
        models.MedicalRecord.id == medicalRecordId
    ).update({"medications": medications.medications})
    db.commit()
    return {"message": "Medical Record (medications) updated successfully"}


@router.put(
    "/update/medicalRecord/surgicalHistory/{userId}/{medicalRecordId}",
    description="Update surgical history.",
)
async def update_surgical_history(
    surgical_history: schemas.SurgicalHistoryUpdate,
    userId: int,
    medicalRecordId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    db.query(models.MedicalRecord).filter(
        models.MedicalRecord.id == medicalRecordId
    ).update({"surgicalHistory": surgical_history.surgicalHistory})
    db.commit()
    return {"message": "Medical Record (surgicalHistory) updated successfully"}


@router.put(
    "/update/medicalRecord/chronicConditions/{userId}/{medicalRecordId}",
    description="Update chronic conditions.",
)
async def update_chronic_conditions(
    chronic_conditions: schemas.ChronicConditionsUpdate,
    userId: int,
    medicalRecordId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    db.query(models.MedicalRecord).filter(
        models.MedicalRecord.id == medicalRecordId
    ).update({"chronicConditions": chronic_conditions.chronicConditions})
    db.commit()
    return {"message": "Medical Record (chronicConditions) updated successfully"}


@router.put(
    "/update/medicalRecord/pastConditions/{userId}/{medicalRecordId}",
    description="Update past conditions.",
)
async def update_past_conditions(
    past_conditions: schemas.PastConditionsUpdate,
    userId: int,
    medicalRecordId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    db.query(models.MedicalRecord).filter(
        models.MedicalRecord.id == medicalRecordId
    ).update({"pastConditions": past_conditions.pastConditions})
    db.commit()
    return {"message": "Medical Record (pastConditions) updated successfully"}


@router.put(
    "/update/medicalRecord/allergies/{userId}/{medicalRecordId}",
    description="Update allergies.",
)
async def update_allergies(
    allergies: schemas.AllergiesUpdate,
    userId: int,
    medicalRecordId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    db.query(models.MedicalRecord).filter(
        models.MedicalRecord.id == medicalRecordId
    ).update({"allergies": allergies.allergies})
    db.commit()
    return {"message": "Medical Record (allergies) updated successfully"}


@router.put(
    "/update/medicalRecord/vaccine/{userId}/{medicalRecordId}",
    description="Update vaccine record.",
)
async def update_vaccine(
    vaccine: schemas.VaccineUpdate,
    userId: int,
    medicalRecordId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    db.query(models.MedicalRecord).filter(
        models.MedicalRecord.id == medicalRecordId
    ).update({"vaccine": vaccine.vaccine})
    db.commit()
    return {"message": "Medical Record (vaccine) updated successfully"}


@router.put(
    "/update/medicalRecord/healthCondition/{userId}/{medicalRecordId}",
    description="Update health condition.",
)
async def update_health_condition(
    health_condition: schemas.HealthConditionUpdate,
    userId: int,
    medicalRecordId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    db.query(models.MedicalRecord).filter(
        models.MedicalRecord.id == medicalRecordId
    ).update({"healthCondition": health_condition.healthCondition})
    db.commit()
    return {"message": "Medical Record (healthCondition) updated successfully"}


@router.put(
    "/update/medicalRecord/treatment/{userId}/{medicalRecordId}",
    description="Update treatment.",
)
async def update_treatment(
    treatment: schemas.TreatmentUpdate,
    userId: int,
    medicalRecordId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    db.query(models.MedicalRecord).filter(
        models.MedicalRecord.id == medicalRecordId
    ).update({"treatment": treatment.treatment})
    db.commit()
    return {"message": "Medical Record (treatment) updated successfully"}


@router.put(
    "/update/medicalRecord/note/{userId}/{medicalRecordId}",
    description="Update notes.",
)
async def update_note(
    note: schemas.NoteUpdate,
    userId: int,
    medicalRecordId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    db.query(models.MedicalRecord).filter(
        models.MedicalRecord.id == medicalRecordId
    ).update({"notes": note.note})
    db.commit()
    return {"message": "Medical Record (note) updated successfully"}


# ─── Delete ──────────────────────────────────────────────────────────────────

@router.delete(
    "/delete/medicalRecord/{userId}/{medicalRecordId}",
    description="Delete a medical record.",
)
async def delete_medical_record(
    userId: int,
    medicalRecordId: int,
    current_user=Depends(deps.get_current_user),
    db: Session = Depends(database.get_db),
):
    record = db.query(models.MedicalRecord).filter(
        models.MedicalRecord.id == medicalRecordId
    ).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical Record not found.")

    db.delete(record)
    db.commit()
    return {"message": "Medical Record deleted successfully"}
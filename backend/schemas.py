from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Optional


# ─── Auth ────────────────────────────────────────────────────────────────────

class UserLogin(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    accessToken: str
    role: str
    userId: int


class TokenData(BaseModel):
    user_id: Optional[int] = None


# ─── FCM ─────────────────────────────────────────────────────────────────────

class FCM(BaseModel):
    fcmToken: str
    userId: int


# ─── User ────────────────────────────────────────────────────────────────────

class User(BaseModel):
    userId: int
    firstName: str
    lastName: str
    email: str
    userName: str
    createdAt: str
    phone: str
    age: Optional[int] = None
    profilePicture: Optional[str] = None
    role: str


class UserSignup(BaseModel):
    userName: str
    email: str
    password: str
    firstName: str
    lastName: str
    phone: str


class AddUser(UserSignup):
    role: str


class UpdateUser(BaseModel):
    userName: str
    email: str
    password: str
    firstName: str
    lastName: str
    phoneNumber: Optional[str] = None
    age: Optional[int] = None
    profilePicture: str


class UpdateUserAdmin(UpdateUser):
    userId: int
    role: str


# ─── Doctor ──────────────────────────────────────────────────────────────────

class Doctor(BaseModel):
    doctorId: int
    firstName: str
    lastName: str
    email: str
    userName: str
    createdAt: str
    rating: Optional[int] = None
    numberOfRating: Optional[int] = None
    price: int
    profilePicture: Optional[str] = None
    role: str


class DoctorList(BaseModel):
    title: Optional[str] = None
    link: Optional[str] = None
    thumbnail: Optional[str] = None
    id: Optional[int] = None
    numberOfReviews: Optional[int] = None
    avarageRating: Optional[float] = None


class DoctorLoginResponse(BaseModel):
    accessToken: str
    doctor: Doctor


class AddDoctor(BaseModel):
    email: str
    password: str
    firstName: str
    lastName: str
    price: int
    profilePic: Optional[str] = None


class UpdateDoctor(BaseModel):
    userName: str
    email: str
    password: str
    firstName: str
    lastName: str
    profilePic: str
    price: int


class UpdateDoctorAdmin(UpdateDoctor):
    doctorId: int


# ─── Patient ────────────────────────────────────────────────────────────────

class Patient(BaseModel):
    id: int
    age: int
    firstName: str
    lastName: str
    parentFirstName: str
    parentLastName: str
    parentPhoneNumber: str
    gender: str
    parentId: int


class PatientResponse(BaseModel):
    id: Optional[int] = None
    age: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    parentFirstName: Optional[str] = None
    parentLastName: Optional[str] = None
    parentPhoneNumber: Optional[str] = None
    gender: Optional[str] = None
    parentId: Optional[int] = None


class AddPatient(BaseModel):
    firstName: str
    lastName: str
    age: int
    gender: str
    parentId: int


class UpdatePatient(BaseModel):
    age: int
    firstName: str
    lastName: str
    gender: str


class ReturnPatient(BaseModel):
    firstName: str
    lastName: str
    parentFirstName: str
    parentLastName: str
    parentPic: str
    age: int
    id: int


class PatientListItem(BaseModel):
    parentPic: str
    patientFirstName: str
    patientLastName: str
    parentFirstName: str
    parentLastName: str
    patientId: int


# ─── Appointment ─────────────────────────────────────────────────────────────

class AddAppointment(BaseModel):
    parentId: int
    doctorId: int
    patientId: int
    appointmentDate: str
    From: str
    To: str
    isTaken: bool

    @field_validator("appointmentDate")
    @classmethod
    def validate_appointment_date(cls, value):
        try:
            datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise ValueError('appointmentDate must be in the format "dd/mm/yyyy"')
        return value


class AppointmentResponse(BaseModel):
    id: int
    parentId: int
    doctorId: int
    appointmentDate: str
    From: str
    To: str
    isTaken: bool


class AllAppointment(BaseModel):
    appointmentId: int
    parentId: int
    patientId: int
    patientFirstName: str
    parentFirstName: str
    parentLastName: str
    doctorId: int
    doctorFirstName: str
    doctorLastName: str
    parentPic: str
    appointmentDate: str
    From: int
    To: int
    isTaken: bool


class UpdateAppointment(BaseModel):
    doctorId: Optional[int] = None
    appointmentDate: Optional[str] = None
    From: Optional[str] = None
    To: Optional[str] = None
    isTaken: Optional[bool] = None


# ─── Medical Record ─────────────────────────────────────────────────────────

class MedicalRecordResponse(BaseModel):
    id: int
    patientId: int
    notes: str
    treatment: str
    createdAt: str
    healthCondition: str
    vaccine: str
    allergies: str
    pastConditions: str
    chronicConditions: str
    surgicalHistory: str
    medications: str
    radiologyReport: str


class UpdateMedicalRecord(BaseModel):
    notes: Optional[str] = None
    treatment: Optional[str] = None
    healthCondition: Optional[str] = None
    vaccine: Optional[str] = None
    allergies: Optional[str] = None
    pastConditions: Optional[str] = None
    chronicConditions: Optional[str] = None
    surgicalHistory: Optional[str] = None
    medications: Optional[str] = None
    radiologyReport: Optional[str] = None


# Individual field update schemas (kept for backwards compatibility with existing API)
class NoteUpdate(BaseModel):
    note: str

class TreatmentUpdate(BaseModel):
    treatment: str

class HealthConditionUpdate(BaseModel):
    healthCondition: str

class VaccineUpdate(BaseModel):
    vaccine: str

class AllergiesUpdate(BaseModel):
    allergies: str

class PastConditionsUpdate(BaseModel):
    pastConditions: str

class ChronicConditionsUpdate(BaseModel):
    chronicConditions: str

class SurgicalHistoryUpdate(BaseModel):
    surgicalHistory: str

class MedicationsUpdate(BaseModel):
    medications: str

class RadiologyReportUpdate(BaseModel):
    radiologyReport: str


# ─── Reviews ────────────────────────────────────────────────────────────────

class ReviewCreate(BaseModel):
    parentId: int
    doctorId: int
    review: str
    rating: int


class ReviewResponse(BaseModel):
    reviewerName: str
    doctorName: str
    review: str
    rating: int


# ─── Analytics ──────────────────────────────────────────────────────────────

class BarChart(BaseModel):
    number: int
    stars: int


class AvgRating(BaseModel):
    avgRating: float
    count: int
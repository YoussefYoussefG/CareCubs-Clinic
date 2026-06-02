from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date, Index, func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "user"

    userId = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    userName = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    googleId = Column(String)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    PhoneNumber = Column(String)
    age = Column(Integer)
    profilePicture = Column(String)
    role = Column(String, nullable=False, index=True)

    appointments = relationship("Appointment", back_populates="user")
    patients = relationship("Patient", back_populates="parent")


class Doctor(Base):
    __tablename__ = "doctor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    userName = Column(String, index=True)
    password = Column(String, nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    rating = Column(Integer)
    numberOfRating = Column(Integer)
    price = Column(Integer, nullable=False)
    profilePicture = Column(String)
    role = Column(String, nullable=False)

    appointments = relationship("Appointment", back_populates="doctor")
    reviews = relationship("Review", back_populates="doctor")


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    parentFirstName = Column(String, nullable=False)
    parentLastName = Column(String, nullable=False)
    parentPhoneNumber = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    parentId = Column(Integer, ForeignKey("user.userId"), nullable=False)

    parent = relationship("User", back_populates="patients")
    medical_records = relationship("MedicalRecord", back_populates="patient")


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parentId = Column(Integer, ForeignKey("user.userId"), nullable=False)
    doctorId = Column(Integer, ForeignKey("doctor.id"), nullable=False)
    patientId = Column(Integer, ForeignKey("patient.id"), nullable=False)
    appointmentDate = Column(Date, nullable=False, index=True)
    fromTime = Column(String, nullable=False)
    toTime = Column(String, nullable=False)
    isTaken = Column(Boolean, default=False)
    Paid = Column(Boolean, default=False)

    user = relationship("User", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")


class MedicalRecord(Base):
    __tablename__ = "medical_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    patientId = Column(Integer, ForeignKey("patient.id"), nullable=False, index=True)
    notes = Column(String, default="None")
    treatment = Column(String, default="None")
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    healthCondition = Column(String, default="None")
    vaccine = Column(String, default="None")
    allergies = Column(String, default="None")
    pastConditions = Column(String, default="None")
    chronicConditions = Column(String, default="None")
    surgicalHistory = Column(String, default="None")
    medications = Column(String, default="None")
    radiologyReport = Column(String, default="None")

    patient = relationship("Patient", back_populates="medical_records")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parentId = Column(Integer, ForeignKey("user.userId"), nullable=False)
    doctorId = Column(Integer, ForeignKey("doctor.id"), nullable=False)
    review = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    doctor = relationship("Doctor", back_populates="reviews")


class MRAccess(Base):
    __tablename__ = "mr_access"

    id = Column(Integer, primary_key=True, autoincrement=True)
    patientId = Column(Integer, ForeignKey("patient.id"), nullable=False)
    doctorId = Column(Integer, ForeignKey("doctor.id"), nullable=False)
    access = Column(Boolean, default=True)


class FCMToken(Base):
    __tablename__ = "FCM"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fcmToken = Column(String, nullable=False)
    userId = Column(Integer, ForeignKey("user.userId"), nullable=False)

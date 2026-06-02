from database import SessionLocal, engine, Base
import models
import utils

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Check if user already exists
user = db.query(models.User).filter(models.User.userName == "saied").first()
if not user:
    # Create the test user 'saied' with password '1234'
    hashed_pwd = utils.hash("1234")
    new_user = models.User(
        userName="saied",
        email="saied@example.com",
        password=hashed_pwd,
        firstName="Saied",
        lastName="Test",
        PhoneNumber="1234567890",
        role="customer",
        profilePicture="https://i.imgur.com/9g7aq8u.png"
    )
    db.add(new_user)
    db.commit()
    print("Test user 'saied' with password '1234' created successfully!")
else:
    print("Test user 'saied' already exists.")

# Also add a doctor so they can test doctor login
doctor = db.query(models.Doctor).filter(models.Doctor.userName == "doctor").first()
if not doctor:
    hashed_pwd = utils.hash("1234")
    new_doctor = models.Doctor(
        userName="doctor",
        email="doctor@example.com",
        password=hashed_pwd,
        firstName="Test",
        lastName="Doctor",
        price=100,
        role="doctor",
        profilePicture="https://i.imgur.com/9g7aq8u.png"
    )
    db.add(new_doctor)
    db.commit()
    print("Test doctor 'doctor' with password '1234' created successfully!")

db.close()

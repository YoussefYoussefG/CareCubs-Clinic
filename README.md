# CareCubs Clinic Management System

## Overview

Welcome to the **CareCubs Clinic Management System**, a comprehensive solution designed to streamline the operations of a pediatric clinic. This system comprises a modern web application, a scalable Python backend, and a mobile application, each tailored to meet the needs of patients, doctors, and clinic staff. 

### Web Application

The web application includes the following portals:
- **Patient Portal:** Enables patients and their guardians to book appointments, view medical records, and communicate with healthcare providers.
- **Doctor Portal:** Provides doctors with tools to manage patient information, schedule appointments, and access medical histories.
- **Staff Portal:** Allows clinic staff to handle administrative tasks, manage patient flow, and coordinate between different departments.
- **Admin Panel:** Offers administrative capabilities for managing user roles, monitoring system performance, and configuring clinic settings.

### Backend System
A fast and secure REST API built with **Python, FastAPI, and SQLAlchemy**. It features secure JWT authentication, SQLite/PostgreSQL database support, and automated background tasks for appointment reminders via Firebase Cloud Messaging.

### Mobile Application

The mobile application aims to enhance user experience by providing access to the following portals on the go:
- **Patient Portal:** Similar to the web version, this allows patients and their guardians to manage appointments, view medical records, and communicate with doctors.
- **Doctor Portal:** Enables doctors to access patient information, manage appointments, and stay updated with clinic activities from their mobile devices.

---

## Features

### Web Application
- **Landing Page:**
  ![Demo Video](GIFs/landingPageDemo.gif)
  
- **Patient Portal:**
  - Appointment scheduling & Medical record access
  ![Demo Video](GIFs/patientPortalDemo.gif)

- **Doctor Portal:**
  - Patient information & Appointment management
  ![Demo Video](GIFs/doctorPortalDemo.gif)

- **Admin Panel:**
  - User role management & System monitoring
  ![Demo Video](GIFs/adminPanelDemo.gif)

---

## Getting Started

### Prerequisites
- **Node.js** (v18 or newer)
- **Python** (v3.10 or newer)
- Web browser (for web application)
- Android device (for mobile application)

### 1. Backend Setup (FastAPI)

1. Clone the repository and open the project directory:
    ```bash
    git clone https://github.com/YoussefYoussefG/CareCubs-Clinic.git
    cd CareCubs-Clinic
    ```
2. Create and activate a Python virtual environment:
    ```bash
    # On Linux/macOS
    python3 -m venv venv
    source venv/bin/activate
    
    # On Windows
    python -m venv venv
    venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Start the backend server:
    ```bash
    uvicorn main:app --reload --port 8000
    ```
    *Note: The backend will automatically fall back to a local SQLite database (`carecubs_test.db`) if no Supabase `DB_URL` is configured in your `.env` file.*
    
    The API documentation will be available at `http://localhost:8000/docs`.

### 2. Frontend Setup (Next.js)

1. Open a new terminal and navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2. Install dependencies:
    ```bash
    npm install
    ```
3. Set up environment variables. Create a `.env.local` file inside the `frontend` directory:
    ```bash
    NEXT_PUBLIC_SERVER_NAME="http://localhost:8000"
    ```
4. Run the application:
    ```bash
    npm run dev
    ```
5. Open your web browser and navigate to:
    ```
    http://localhost:3000
    ```

### 3. Mobile Application (Android)
- Download the APK file from the link below:
  [Download CareCubs APK](https://drive.google.com/uc?export=download&id=1SytD4rQxmdjy4ixm1Odtz4UqUjFXSlVc)
- Install the APK directly on your Android device.

---

## Deployment
For detailed deployment instructions for Supabase, Render, and Vercel, please check out the included `DEPLOYMENT_GUIDE.md` and `SUPABASE_GUIDE.md` documents.

## Contact

If you have any questions or need further assistance, feel free to reach out:
- **Email:** yg.youssef.gamal16@gmail.com
- **Issues:** [GitHub Issues](https://github.com/YoussefYoussefG/CareCubs-Clinic/issues)
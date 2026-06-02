# CareCubs Clinic Deployment Guide

This guide covers deploying the backend to Render/Railway and the frontend to Vercel.

## 1. Backend Deployment (Render / Railway)

### Using Render
1. Create a new **Web Service** on [Render](https://render.com).
2. Connect your GitHub repository.
3. Configure settings:
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Go to the **Environment Variables** section and add:
   - `DB_URL`: Your Supabase connection string (see `SUPABASE_GUIDE.md`)
   - `SECRET_KEY`: A strong JWT secret key.
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: E.g., `60`

### Using Railway
1. Create a **New Project** on [Railway](https://railway.app).
2. Connect your GitHub repository.
3. Railway will automatically detect the Python environment via `requirements.txt`.
4. Go to **Variables** and add the same environment variables as above (`DB_URL`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`).
5. Ensure Railway tracks the start command correctly (or explicitly set `uvicorn main:app --host 0.0.0.0 --port $PORT`).

## 2. Frontend Deployment (Vercel)

1. Sign up on [Vercel](https://vercel.com/) and click **Add New** > **Project**.
2. Import your GitHub repository.
3. Keep the default settings (Framework Preset: Next.js).
4. Set the Root Directory to `frontend`.
5. Add any necessary Environment Variables (e.g., your Backend's deployed API URL).
   - `NEXT_PUBLIC_API_URL`: The deployed URL (e.g., `https://carecubs-api.onrender.com/`)
6. Click **Deploy**.

## 3. Mandatory Environment Variables Checklist

**Backend:**
- `DB_URL`: PostgreSQL connection string (Supabase).
- `SECRET_KEY`: Random string for JWT tokens.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiry in minutes (default: `60`).
- `FIREBASE_CREDENTIALS_JSON`: Full Firebase service account JSON as a string (recommended for deployment).
- `FIREBASE_KEY_PATH`: Path to `firebase_key.json` file (fallback for local development, default: `firebase_key.json`).
- `FIREBASE_PROJECT_ID`: Firebase project ID for FCM (default: `pulse-pediatric`).

**Frontend:**
- `NEXT_PUBLIC_API_URL`: Backend API endpoint URL.
- `NEXT_PUBLIC_SERVER_NAME`: Backend server URL (used by some components).
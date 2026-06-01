# Supabase Migration & Setup Guide

## 1. Create a Supabase Project
1. Log in to [Supabase](https://supabase.com/) and click **New Project**.
2. Select your organization, name your project (e.g., *CareCubs Clinic*), and securely store the **Database Password**.
3. Choose the region closest to your primary users.

## 2. Retrieve the Database URI
1. Go to your project's **Settings** > **Database**.
2. Scroll to the **Connection string** section.
3. Select the `URI` tab (or JDBC format if supported) and replace `[YOUR-PASSWORD]` with the database password from step 1.
4. Your connection string will look similar to this:
   ```env
   postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```

## 3. Update Environment Variables
In your backend directory, create or update your `.env` file with the Supabase URI string:
```env
DB_URL="postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres"
```

## 4. Alembic Migration (Optional)
If you want to use Alembic for handling schema migrations:

1. Install Alembic:
   ```bash
   pip install alembic psycopg2-binary
   ```
2. Initialize Alembic:
   ```bash
   alembic init alembic
   ```
3. Update `alembic.ini`:
   ```ini
   sqlalchemy.url = postgresql://... (Use your Supabase URI pointer or load it dynamically)
   ```
4. Configure `alembic/env.py` to import your Base model:
   ```python
   import models
   target_metadata = models.Base.metadata
   ```
5. Generate an initial migration:
   ```bash
   alembic revision --autogenerate -m "Initial Supabase schema"
   alembic upgrade head
   ```
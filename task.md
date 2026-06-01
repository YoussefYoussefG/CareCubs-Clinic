# CareCubs Clinic Evolution — Task Tracker

## Phase 1: .gitignore Cleanup
- [x] Replace `.gitignore` with comprehensive version
- [x] Remove `firebase_key.json` from tracking (add to env vars)
- [x] Delete unnecessary root-level files (`__inti__.py`, `requirments.txt`, `fluttericon.yaml`)
- [x] Delete root-level `package.json`, `package-lock.json`, `node_modules/`
- [x] Delete `Backend/` directory (older duplicate)
- [x] Delete `Backend(Express)/` directory (incomplete rewrite)
- [x] Clean `__pycache__/` directories

## Phase 2: Backend Improvements
- [x] 2.1 Security Fixes
  - [x] Fix `oauth2.py` — remove self-import, fix deprecations, reduce token expiry
  - [x] Create `deps.py` — shared auth dependencies (`get_current_user`, `require_admin`, `require_doctor`)
  - [x] Implement actual password validation in `utils.py`
- [x] 2.2 Architecture & Code Quality
  - [x] Rename `DataBase.py` → `database.py`, modernize
  - [x] Fix `models.py` — typos, naming, indexes, relationships
  - [x] Fix `schemas.py` — duplicates, typos, Pydantic v2 style
  - [x] Refactor `routes/auth.py`
  - [ ] Refactor `routes/doctor.py`
  - [ ] Refactor `routes/appointment.py`
  - [ ] Refactor `routes/patient.py`
  - [ ] Refactor `routes/user.py`
  - [x] Refactor `routes/MedicalRecord.py` → `routes/medical_record.py`
  - [ ] Refactor `routes/reviews.py`
  - [ ] Refactor `routes/notification.py`
- [ ] 2.3 Fix `scheduler.py` — remove keep_awake, env-based Firebase creds
- [ ] 2.4 Update `main.py` to use new module names
- [ ] 2.5 Update `requirements.txt` — clean and pin versions

## Phase 3: Frontend Improvements
- [ ] Create API service layer (`services/api.ts`)
- [ ] Create auth context for token management
- [ ] Remove unused deps (`express`, `jsonwebtoken`, `react-router-dom`)
- [ ] Add error handling and loading states
- [ ] Add SEO meta tags
- [ ] Add error boundaries

## Phase 4: Supabase Migration Guide
- [ ] Write Supabase setup guide with connection string format
- [ ] Add Alembic migration support (optional)

## Phase 5: Deployment Guide
- [ ] Write Vercel deployment guide for frontend
- [ ] Write backend deployment guide (Render/Railway)
- [ ] Document environment variables needed

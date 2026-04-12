# ChronicCare — Module 2: Chronic Disease Management System

## Setup Steps

### 1. Database
Make sure you have MongoDB running locally or on Atlas. Update the `.env` if necessary.

### 2. Backend
1. `cd backend`
2. Create virtual env: `python -m venv venv`
3. Activate env: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. `pip install -r requirements.txt`
5. `uvicorn main:app --reload` (Runs on `http://localhost:8000`)

### 3. Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev` (Runs on `http://localhost:5173`)

## Environment Variables (.env)
Required inside the `/backend/.env` file:
```
MONGO_URI=mongodb://localhost:27017
PORT=8000
MODULE1_URL=http://localhost:8001/api/module1
MODULE19_URL=http://localhost:8019/api
MODULE25_URL=http://localhost:8025/api
MODULE33_URL=http://localhost:8033/api
JWT_SECRET=super_secret_key_change_in_production
```

## API Endpoint Reference
### Patients
- `GET /api/module1/patient/{id}` - Fetch from Module 1
- `GET /api/patients`
- `GET /api/patients/{id}`
- `POST /api/patients`

### Chronic Diseases
- `GET /api/diseases`
- `POST /api/diseases`

### Diagnoses
- `GET /api/diagnoses/patient/{id}`
- `POST /api/diagnoses`

### Clinical Metrics
- `GET /api/metrics/diagnosis/{id}`
- `POST /api/metrics` -> background task to Mock Module 25

### Disease Episodes
- `GET /api/episodes/diagnosis/{id}`
- `POST /api/episodes`
- `PATCH /api/episodes/{id}`

### Risk Assessments
- `GET /api/risks/patient/{id}`
- `POST /api/risks`

### Treatment Plans
- `GET /api/plans/diagnosis/{id}`
- `POST /api/plans` -> background task to Mock Modules 19 & 33

### Medication Adherence
- `GET /api/adherence/plan/{id}`
- `POST /api/adherence`

### Integration Logs
- `GET /api/integrations`

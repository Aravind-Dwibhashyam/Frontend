from fastapi import APIRouter, HTTPException, Depends
from typing import List
from db.client import get_database
from models.patient import Patient, PatientCreate
from services.module1 import fetch_patient_from_module1

router = APIRouter(prefix="/api", tags=["Patients"])

@router.get("/module1/patient/{patient_id}")
async def fetch_and_save_module1_patient(patient_id: str):
    db = get_database()
    patient_data = await fetch_patient_from_module1(patient_id)
    if not patient_data:
        raise HTTPException(status_code=404, detail="Patient not found in Module-1 or Module-1 is down")
    
    # Store patient locally
    existing = await db.patients.find_one({"patient_id": patient_data.get("patient_id")})
    if not existing:
        patient_create = PatientCreate(**patient_data)
        await db.patients.insert_one(patient_create.model_dump(mode='json'))
        return {"message": "Patient fetched from Module-1 and saved.", "patient": patient_data}
    return {"message": "Patient already exists.", "patient": existing}

@router.get("/patients", response_model=List[Patient])
async def get_all_patients():
    db = get_database()
    patients = await db.patients.find().to_list(1000)
    return patients

@router.get("/patients/{patient_id}")
async def get_patient_details(patient_id: str):
    db = get_database()
    patient = await db.patients.find_one({"patient_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    diagnoses = await db.patient_diagnoses.find({"patient_id": patient_id}).to_list(100)
    risks = await db.risk_assessments.find({"patient_id": patient_id}).to_list(100)
    
    diagnosis_ids = [d.get("diagnosis_id") for d in diagnoses if d.get("diagnosis_id")]
    metrics = await db.clinical_metrics.find({"diagnosis_id": {"$in": diagnosis_ids}}).to_list(100)
    episodes = await db.disease_episodes.find({"diagnosis_id": {"$in": diagnosis_ids}}).to_list(100)
    plans = await db.treatment_plans.find({"diagnosis_id": {"$in": diagnosis_ids}}).to_list(100)
    
    plan_ids = [p.get("plan_id") for p in plans if p.get("plan_id")]
    adherences = await db.medication_adherences.find({"plan_id": {"$in": plan_ids}}).to_list(100)
    
    if patient and "_id" in patient:
        patient["_id"] = str(patient["_id"])
        
    for lst in [diagnoses, metrics, risks, episodes, plans, adherences]:
        for item in lst:
            if "_id" in item: item["_id"] = str(item["_id"])
        
    return {
        "patient": patient,
        "diagnoses": diagnoses,
        "metrics": metrics,
        "risks": risks,
        "episodes": episodes,
        "plans": plans,
        "adherence": adherences
    }

@router.post("/patients", response_model=Patient)
async def create_patient_manually(patient: PatientCreate):
    db = get_database()
    existing = await db.patients.find_one({"patient_id": patient.patient_id})
    if existing:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    patient_dict = patient.model_dump(mode='json')
    result = await db.patients.insert_one(patient_dict)
    
    created_patient = await db.patients.find_one({"_id": result.inserted_id})
    return created_patient

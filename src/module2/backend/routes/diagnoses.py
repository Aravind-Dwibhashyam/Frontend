from fastapi import APIRouter, HTTPException
from typing import List
from db.client import get_database
from models.diagnosis import Diagnosis, DiagnosisCreate

router = APIRouter(prefix="/api/diagnoses", tags=["Diagnoses"])

@router.get("/patient/{patient_id}", response_model=List[Diagnosis])
async def get_diagnoses_for_patient(patient_id: str):
    db = get_database()
    diagnoses = await db.patient_diagnoses.find({"patient_id": patient_id}).to_list(1000)
    return diagnoses

@router.post("/", response_model=Diagnosis)
async def create_diagnosis(diagnosis: DiagnosisCreate):
    db = get_database()
    existing = await db.patient_diagnoses.find_one({"diagnosis_id": diagnosis.diagnosis_id})
    if existing:
        raise HTTPException(status_code=400, detail="Diagnosis already exists")
    
    diagnosis_dict = diagnosis.model_dump(mode='json')
    result = await db.patient_diagnoses.insert_one(diagnosis_dict)
    created_diagnosis = await db.patient_diagnoses.find_one({"_id": result.inserted_id})
    return created_diagnosis

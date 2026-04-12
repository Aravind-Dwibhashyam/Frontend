from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from db.client import get_database
from services.demographics import DemographicsAPI

router = APIRouter(prefix="/api/patients", tags=["Patients"])

@router.get("", response_model=List[Dict[str, Any]])
async def get_all_patients():
    """Fetch all actual patients directly from Module 1 API"""
    patients = await DemographicsAPI.list_patients()
    return patients

@router.get("/{patient_id}")
async def get_patient_details(patient_id: str):
    """Fetch patient profile from Module 1 and locally join Module 2 clinical records"""
    patient_data = await DemographicsAPI.get_patient(patient_id)
    if not patient_data:
        raise HTTPException(status_code=404, detail="Patient not found in Demographics Module")
        
    db = get_database()
        
    diagnoses = await db.patient_diagnoses.find({"patient_id": patient_id}).to_list(100)
    risks = await db.risk_assessments.find({"patient_id": patient_id}).to_list(100)
    
    diagnosis_ids = [d.get("diagnosis_id") for d in diagnoses if d.get("diagnosis_id")]
    metrics = await db.clinical_metrics.find({"diagnosis_id": {"$in": diagnosis_ids}}).to_list(100)
    episodes = await db.disease_episodes.find({"diagnosis_id": {"$in": diagnosis_ids}}).to_list(100)
    plans = await db.treatment_plans.find({"diagnosis_id": {"$in": diagnosis_ids}}).to_list(100)
    
    plan_ids = [p.get("plan_id") for p in plans if p.get("plan_id")]
    adherences = await db.medication_adherences.find({"plan_id": {"$in": plan_ids}}).to_list(100)
        
    for lst in [diagnoses, metrics, risks, episodes, plans, adherences]:
        for item in lst:
            if "_id" in item: item["_id"] = str(item["_id"])
        
    return {
        "patient": patient_data,
        "diagnoses": diagnoses,
        "metrics": metrics,
        "risks": risks,
        "episodes": episodes,
        "plans": plans,
        "adherence": adherences
    }

@router.get("/{patient_id}/visits", response_model=List[Dict[str, Any]])
async def get_patient_visits(patient_id: str):
    """Fetch patient visits directly from Module 1 API"""
    visits = await DemographicsAPI.get_patient_visits(patient_id)
    return visits

@router.get("/{patient_id}/summary", response_model=Dict[str, Any])
async def get_patient_summary(patient_id: str):
    """Fetch patient summary directly from Module 1 API"""
    summary = await DemographicsAPI.get_patient_summary(patient_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Patient summary not found")
    return summary

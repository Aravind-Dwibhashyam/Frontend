from fastapi import APIRouter, HTTPException
from typing import List
from db.client import get_database
from models.risk_assessment import RiskAssessment, RiskAssessmentCreate

router = APIRouter(prefix="/api/risks", tags=["Risk Assessments"])

@router.get("/patient/{patient_id}", response_model=List[RiskAssessment])
async def get_risks_for_patient(patient_id: str):
    db = get_database()
    risks = await db.risk_assessments.find({"patient_id": patient_id}).to_list(1000)
    return risks

@router.post("/", response_model=RiskAssessment)
async def create_risk(risk: RiskAssessmentCreate):
    db = get_database()
    existing = await db.risk_assessments.find_one({"assessment_id": risk.assessment_id})
    if existing:
        raise HTTPException(status_code=400, detail="Risk assessment already exists")
    
    risk_dict = risk.model_dump(mode='json')
    result = await db.risk_assessments.insert_one(risk_dict)
    created_risk = await db.risk_assessments.find_one({"_id": result.inserted_id})
    return created_risk

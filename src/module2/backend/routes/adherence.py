from fastapi import APIRouter, HTTPException
from typing import List
from db.client import get_database
from models.medication_adherence import MedicationAdherence, MedicationAdherenceCreate

router = APIRouter(prefix="/api/adherence", tags=["Medication Adherence"])

@router.get("/plan/{plan_id}", response_model=List[MedicationAdherence])
async def get_adherence_for_plan(plan_id: str):
    db = get_database()
    adherences = await db.medication_adherences.find({"plan_id": plan_id}).to_list(1000)
    return adherences

@router.post("/", response_model=MedicationAdherence)
async def create_adherence(adherence: MedicationAdherenceCreate):
    db = get_database()
    existing = await db.medication_adherences.find_one({"adherence_id": adherence.adherence_id})
    if existing:
        raise HTTPException(status_code=400, detail="Adherence log already exists")
    
    adherence_dict = adherence.model_dump(mode='json')
    result = await db.medication_adherences.insert_one(adherence_dict)
    created_adherence = await db.medication_adherences.find_one({"_id": result.inserted_id})
    return created_adherence

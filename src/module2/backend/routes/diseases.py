from fastapi import APIRouter, HTTPException
from typing import List
from db.client import get_database
from models.chronic_disease import ChronicDisease, ChronicDiseaseCreate

router = APIRouter(prefix="/api/diseases", tags=["Diseases"])

@router.get("/", response_model=List[ChronicDisease])
async def get_all_diseases():
    db = get_database()
    diseases = await db.chronic_diseases.find().to_list(1000)
    return diseases

@router.post("/", response_model=ChronicDisease)
async def create_disease(disease: ChronicDiseaseCreate):
    db = get_database()
    existing = await db.chronic_diseases.find_one({"disease_id": disease.disease_id})
    if existing:
        raise HTTPException(status_code=400, detail="Disease already exists")
    
    disease_dict = disease.model_dump(mode='json')
    result = await db.chronic_diseases.insert_one(disease_dict)
    created_disease = await db.chronic_diseases.find_one({"_id": result.inserted_id})
    return created_disease

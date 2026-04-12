from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from db.client import get_database
from models.treatment_plan import TreatmentPlan, TreatmentPlanCreate
from services.module19 import send_prescription_to_module19
from services.module33 import send_progression_to_module33

router = APIRouter(prefix="/api/plans", tags=["Treatment Plans"])

@router.get("/diagnosis/{diagnosis_id}", response_model=List[TreatmentPlan])
async def get_plans_for_diagnosis(diagnosis_id: str):
    db = get_database()
    plans = await db.treatment_plans.find({"diagnosis_id": diagnosis_id}).to_list(1000)
    return plans

@router.post("/", response_model=TreatmentPlan)
async def create_plan(plan: TreatmentPlanCreate, bg_tasks: BackgroundTasks):
    db = get_database()
    existing = await db.treatment_plans.find_one({"plan_id": plan.plan_id})
    if existing:
        raise HTTPException(status_code=400, detail="Plan already exists")
    
    plan_dict = plan.model_dump(mode='json')
    result = await db.treatment_plans.insert_one(plan_dict)
    created_plan = await db.treatment_plans.find_one({"_id": result.inserted_id})
    
    # We need diagnosis details for patient_id, disease_id
    diagnosis = await db.patient_diagnoses.find_one({"diagnosis_id": plan.diagnosis_id})
    if diagnosis:
        disease = await db.chronic_diseases.find_one({"disease_id": diagnosis["disease_id"]})
        disease_name = disease["name"] if disease else "Unknown"

        bg_tasks.add_task(
            send_prescription_to_module19,
            patient_id=diagnosis["patient_id"],
            plan_id=plan.plan_id,
            medications="Assume from Plan", # Not fully in schema, mocked
            doctor_id=plan.doctor_id
        )
        bg_tasks.add_task(
            send_progression_to_module33,
            patient_id=diagnosis["patient_id"],
            diagnosis_id=plan.diagnosis_id,
            disease_name=disease_name,
            treatment_plan=plan.goal,
            history="New plan initiated"
        )

    return created_plan

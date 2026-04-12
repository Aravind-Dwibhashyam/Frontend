from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from db.client import get_database
from models.clinical_metric import ClinicalMetric, ClinicalMetricCreate
from services.module25 import send_vitals_to_module25

router = APIRouter(prefix="/api/metrics", tags=["Clinical Metrics"])

@router.get("/diagnosis/{diagnosis_id}", response_model=List[ClinicalMetric])
async def get_metrics_for_diagnosis(diagnosis_id: str):
    db = get_database()
    metrics = await db.clinical_metrics.find({"diagnosis_id": diagnosis_id}).to_list(1000)
    return metrics

@router.post("/", response_model=ClinicalMetric)
async def create_metric(metric: ClinicalMetricCreate, bg_tasks: BackgroundTasks):
    db = get_database()
    existing = await db.clinical_metrics.find_one({"metric_id": metric.metric_id})
    if existing:
        raise HTTPException(status_code=400, detail="Metric already exists")
    
    metric_dict = metric.model_dump(mode='json')
    result = await db.clinical_metrics.insert_one(metric_dict)
    created_metric = await db.clinical_metrics.find_one({"_id": result.inserted_id})
    
    # We need patient_id to send to Module 25, which means fetching diagnosis then patient
    diagnosis = await db.patient_diagnoses.find_one({"diagnosis_id": metric.diagnosis_id})
    if diagnosis:
        # Fire async task
        bg_tasks.add_task(
            send_vitals_to_module25,
            patient_id=diagnosis["patient_id"],
            metric_type=metric.metric_type,
            value=metric.value,
            unit=metric.unit,
            recorded_at=metric.recorded_at.isoformat()
        )

    return created_metric

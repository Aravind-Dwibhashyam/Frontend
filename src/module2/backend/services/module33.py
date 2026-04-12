import httpx
from db.client import settings
from .demographics import log_integration
import asyncio

async def send_progression_to_module33(patient_id: str, diagnosis_id: str, disease_name: str, treatment_plan: str, history: str):
    payload = {
        "patient_id": patient_id,
        "diagnosis_id": diagnosis_id,
        "disease_name": disease_name,
        "treatment_plan": treatment_plan,
        "history": history
    }
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.MODULE33_URL}/progression"
            response = await client.post(url, json=payload, timeout=2.0)
            status = response.status_code
            result = "success" if 200 <= status < 300 else "failed"
    except Exception as e:
        status = 0
        result = "mock"
    
    await log_integration("Module-33", f"Progression for {patient_id} ({disease_name})", status, result)

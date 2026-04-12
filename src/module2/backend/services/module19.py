import httpx
from db.client import settings
from .module1 import log_integration
import asyncio

async def send_prescription_to_module19(patient_id: str, plan_id: str, medications: str, doctor_id: str):
    payload = {
        "patient_id": patient_id,
        "plan_id": plan_id,
        "medications": medications,
        "doctor_id": doctor_id
    }
    try:
        # Mock actual request to module 19
        async with httpx.AsyncClient() as client:
            url = f"{settings.MODULE19_URL}/prescriptions"
            # It's mock, so we wrap it in a quick timeout and don't care if it fails
            response = await client.post(url, json=payload, timeout=2.0)
            status = response.status_code
            result = "success" if 200 <= status < 300 else "failed"
    except Exception as e:
        status = 0
        result = "mock"
    
    await log_integration("Module-19", f"Prescription for {patient_id}", status, result)

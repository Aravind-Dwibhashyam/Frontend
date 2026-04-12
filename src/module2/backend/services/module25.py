import httpx
from db.client import settings
from .demographics import log_integration
import asyncio

async def send_vitals_to_module25(patient_id: str, metric_type: str, value: float, unit: str, recorded_at: str):
    payload = {
        "patient_id": patient_id,
        "metric_type": metric_type,
        "value": value,
        "unit": unit,
        "recorded_at": recorded_at
    }
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.MODULE25_URL}/vitals"
            response = await client.post(url, json=payload, timeout=2.0)
            status = response.status_code
            result = "success" if 200 <= status < 300 else "failed"
    except Exception as e:
        status = 0
        result = "mock"
    
    await log_integration("Module-25", f"Vitals {metric_type} for {patient_id}", status, result)

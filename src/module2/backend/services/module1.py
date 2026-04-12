import httpx
from db.client import settings, get_database
from models.integration_log import IntegrationLogCreate
from datetime import datetime
import asyncio

async def log_integration(target: str, payload_summary: str, status: int, result: str):
    db = get_database()
    log = IntegrationLogCreate(
        target_module=target,
        payload_summary=payload_summary,
        http_status=status,
        result=result
    )
    await db.integration_logs.insert_one(log.model_dump())

async def fetch_patient_from_module1(patient_id: str):
    try:
        async with httpx.AsyncClient() as client:
            # According to specs: GET http://module1-service/api/patient/{id}
            url = f"{settings.MODULE1_URL}/patient/{patient_id}"
            response = await client.get(url, timeout=5.0)
            
            if response.status_code == 200:
                await log_integration("Module-1", f"Fetched patient {patient_id}", response.status_code, "success")
                return response.json()
            else:
                await log_integration("Module-1", f"Failed fetching {patient_id}", response.status_code, "failed")
                return None
    except Exception as e:
        await log_integration("Module-1", f"Error string {e}", 500, "failed")
        return None

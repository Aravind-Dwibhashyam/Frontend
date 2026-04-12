import httpx
from typing import Optional, Dict, Any, List
from db.client import settings


from db.client import get_database
from models.integration_log import IntegrationLogCreate

async def log_integration(target: str, payload_summary: str, status: int, result: str):
    db = get_database()
    log = IntegrationLogCreate(
        target_module=target,
        payload_summary=payload_summary,
        http_status=status,
        result=result
    )
    await db.integration_logs.insert_one(log.model_dump())

class DemographicsAPI:
    @staticmethod
    async def get_health() -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.MODULE1_URL}/health", timeout=5.0)
            await log_integration("Module-1", "Health check", response.status_code, "success" if response.status_code == 200 else "failed")
            return response.json() if response.status_code == 200 else {}

    @staticmethod
    async def get_stats() -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.MODULE1_URL}/stats", timeout=5.0)
            await log_integration("Module-1", "Get stats", response.status_code, "success" if response.status_code == 200 else "failed")
            return response.json() if response.status_code == 200 else {}

    @staticmethod
    async def list_patients(name: Optional[str] = None, gender: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        params = {"limit": limit}
        if name: params["name"] = name
        if gender: params["gender"] = gender
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.MODULE1_URL}/patients", params=params, timeout=10.0)
            await log_integration("Module-1", "List patients", response.status_code, "success" if response.status_code == 200 else "failed")
            return response.json() if response.status_code == 200 else []

    @staticmethod
    async def get_patient(patient_id: str) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.MODULE1_URL}/patients/{patient_id}", timeout=10.0)
            status = "success" if response.status_code == 200 else "failed"
            await log_integration("Module-1", f"Get patient {patient_id}", response.status_code, status)
            if response.status_code == 200:
                return response.json()
            return None

    @staticmethod
    async def get_patient_visits(patient_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.MODULE1_URL}/patients/{patient_id}/visits", params={"limit": limit}, timeout=10.0)
            await log_integration("Module-1", f"Get visits for {patient_id}", response.status_code, "success" if response.status_code == 200 else "failed")
            return response.json() if response.status_code == 200 else []

    @staticmethod
    async def get_patient_summary(patient_id: str) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.MODULE1_URL}/patients/{patient_id}/summary", timeout=10.0)
            await log_integration("Module-1", f"Get summary for {patient_id}", response.status_code, "success" if response.status_code == 200 else "failed")
            if response.status_code == 200:
                return response.json()
            return None

    @staticmethod
    async def list_departments() -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.MODULE1_URL}/departments", timeout=10.0)
            await log_integration("Module-1", "List departments", response.status_code, "success" if response.status_code == 200 else "failed")
            return response.json() if response.status_code == 200 else []

    @staticmethod
    async def list_physicians() -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.MODULE1_URL}/physicians", timeout=10.0)
            await log_integration("Module-1", "List physicians", response.status_code, "success" if response.status_code == 200 else "failed")
            return response.json() if response.status_code == 200 else []

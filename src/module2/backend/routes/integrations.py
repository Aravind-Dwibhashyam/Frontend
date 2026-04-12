from fastapi import APIRouter, HTTPException
from typing import List
from db.client import get_database
from models.integration_log import IntegrationLog

router = APIRouter(prefix="/api/integrations", tags=["Integration Logs"])

@router.get("/", response_model=List[IntegrationLog])
async def get_integration_logs():
    db = get_database()
    # Return sorted by timestamp desc
    logs = await db.integration_logs.find().sort("timestamp", -1).to_list(1000)
    return logs

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from services.demographics import DemographicsAPI

router = APIRouter(prefix="/api/demographics", tags=["Demographics Reference (M1)"])

@router.get("/health", response_model=Dict[str, Any])
async def get_m1_health():
    """Proxy health check to Module 1"""
    return await DemographicsAPI.get_health()

@router.get("/stats", response_model=Dict[str, Any])
async def get_m1_stats():
    """Proxy stats to Module 1"""
    return await DemographicsAPI.get_stats()

@router.get("/departments", response_model=List[Dict[str, Any]])
async def list_m1_departments():
    """Proxy departments lookup to Module 1"""
    return await DemographicsAPI.list_departments()

@router.get("/physicians", response_model=List[Dict[str, Any]])
async def list_m1_physicians():
    """Proxy physicians lookup to Module 1"""
    return await DemographicsAPI.list_physicians()

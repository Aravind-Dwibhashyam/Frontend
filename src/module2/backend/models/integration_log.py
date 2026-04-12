from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated
from typing import Optional, Any, Dict
from datetime import datetime

class IntegrationLogBase(BaseModel):
    target_module: str
    payload_summary: str
    http_status: Optional[int] = None
    result: str # success, failed, mock
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class IntegrationLogCreate(IntegrationLogBase):
    pass

class IntegrationLog(IntegrationLogBase):
    id: Annotated[str, BeforeValidator(str)] | None = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True

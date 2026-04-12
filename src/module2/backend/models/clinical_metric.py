from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated
from typing import Optional
from datetime import datetime

class ClinicalMetricBase(BaseModel):
    metric_id: str
    diagnosis_id: str
    metric_type: str
    value: float
    unit: str
    recorded_at: datetime
    doctor_id: str

class ClinicalMetricCreate(ClinicalMetricBase):
    pass

class ClinicalMetric(ClinicalMetricBase):
    id: Annotated[str, BeforeValidator(str)] | None = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True

from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated
from typing import Optional

class RiskAssessmentBase(BaseModel):
    assessment_id: str
    patient_id: str
    risk_score: float
    category: str  # e.g., Low, Moderate, High, Critical

class RiskAssessmentCreate(RiskAssessmentBase):
    pass

class RiskAssessment(RiskAssessmentBase):
    id: Annotated[str, BeforeValidator(str)] | None = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True

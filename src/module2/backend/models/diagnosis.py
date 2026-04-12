from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated
from typing import Optional
from datetime import date

class DiagnosisBase(BaseModel):
    diagnosis_id: str
    patient_id: str
    disease_id: str
    assessment_id: Optional[str] = None
    date_diagnosed: date
    severity_stage: str
    current_status: str
    doctor_id: str

class DiagnosisCreate(DiagnosisBase):
    pass

class Diagnosis(DiagnosisBase):
    id: Annotated[str, BeforeValidator(str)] | None = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True

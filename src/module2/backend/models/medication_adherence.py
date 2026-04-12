from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated
from typing import Optional
from datetime import date

class MedicationAdherenceBase(BaseModel):
    adherence_id: str
    plan_id: str
    log_date: date
    status: str
    reason_skipped: Optional[str] = None

class MedicationAdherenceCreate(MedicationAdherenceBase):
    pass

class MedicationAdherence(MedicationAdherenceBase):
    id: Annotated[str, BeforeValidator(str)] | None = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True

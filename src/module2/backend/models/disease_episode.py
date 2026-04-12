from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated
from typing import Optional, List
from datetime import date

class DiseaseEpisodeBase(BaseModel):
    episode_id: str
    diagnosis_id: str
    start_date: date
    end_date: Optional[date] = None
    severity_levels: str
    triggers: Optional[List[str]] = []
    doctor_id: str

class DiseaseEpisodeCreate(DiseaseEpisodeBase):
    pass

class DiseaseEpisode(DiseaseEpisodeBase):
    id: Annotated[str, BeforeValidator(str)] | None = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True

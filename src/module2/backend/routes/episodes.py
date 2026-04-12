from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from db.client import get_database
from models.disease_episode import DiseaseEpisode, DiseaseEpisodeCreate

router = APIRouter(prefix="/api/episodes", tags=["Disease Episodes"])

class EpisodeUpdate(BaseModel):
    end_date: date

@router.get("/diagnosis/{diagnosis_id}", response_model=List[DiseaseEpisode])
async def get_episodes_for_diagnosis(diagnosis_id: str):
    db = get_database()
    episodes = await db.disease_episodes.find({"diagnosis_id": diagnosis_id}).to_list(1000)
    return episodes

@router.post("/", response_model=DiseaseEpisode)
async def create_episode(episode: DiseaseEpisodeCreate):
    db = get_database()
    existing = await db.disease_episodes.find_one({"episode_id": episode.episode_id})
    if existing:
        raise HTTPException(status_code=400, detail="Episode already exists")
    
    episode_dict = episode.model_dump(mode='json')
    result = await db.disease_episodes.insert_one(episode_dict)
    created_episode = await db.disease_episodes.find_one({"_id": result.inserted_id})
    return created_episode

@router.patch("/{id}", response_model=DiseaseEpisode)
async def update_episode_end_date(id: str, update: EpisodeUpdate):
    db = get_database()
    result = await db.disease_episodes.update_one(
        {"episode_id": id},
        {"$set": {"end_date": update.end_date.isoformat()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Episode not found")
        
    updated_episode = await db.disease_episodes.find_one({"episode_id": id})
    return updated_episode

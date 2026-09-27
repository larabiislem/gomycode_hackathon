"""Strategy routes."""
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any

from brandforge.api.middleware.auth import get_current_user

router = APIRouter(prefix="/api/strategy", tags=["Strategy"])

class StrategyGenerateRequest(BaseModel):
    campaign_goal: str

class PillarsUpdateRequest(BaseModel):
    pillars: List[Dict[str, Any]]

@router.post("/generate")
async def generate_strategy(request: StrategyGenerateRequest, req: Request, user: dict = Depends(get_current_user)):
    """Trigger strategy generation via Strategy Team."""
    return {"status": "success", "strategy": "Draft strategy based on " + request.campaign_goal}

@router.get("/current")
async def get_current_strategy(req: Request, user: dict = Depends(get_current_user)):
    """Return current marketing strategy."""
    return {"status": "success", "strategy": "Q4 Growth Strategy"}

@router.put("/pillars")
async def update_pillars(request: PillarsUpdateRequest, req: Request, user: dict = Depends(get_current_user)):
    """Update content pillars."""
    return {"status": "success", "message": "Pillars updated successfully"}

@router.get("/competitors")
async def get_competitors(req: Request, user: dict = Depends(get_current_user)):
    """Return competitor analysis."""
    return {"status": "success", "competitors": ["Blue Bottle Coffee", "Stumptown", "Counter Culture Coffee"]}

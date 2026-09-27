"""Ads routes."""
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from brandforge.api.middleware.auth import get_current_user

router = APIRouter(prefix="/api/ads", tags=["Ads"])

class CampaignRequest(BaseModel):
    name: str
    budget: float
    target_audience: str

class OptimizationRequest(BaseModel):
    action: str

@router.post("/campaign")
async def launch_campaign(request: CampaignRequest, req: Request, user: dict = Depends(get_current_user)):
    """Launch new campaign via CampaignLaunchWorkflow."""
    return {"status": "success", "message": f"Campaign {request.name} launched"}

@router.get("/campaigns")
async def list_campaigns(req: Request, user: dict = Depends(get_current_user)):
    """List all campaigns."""
    return {"status": "success", "campaigns": []}

@router.put("/optimize/{campaign_id}")
async def optimize_campaign(campaign_id: str, request: OptimizationRequest, req: Request, user: dict = Depends(get_current_user)):
    """Optimize campaign."""
    return {"status": "success", "message": f"Campaign {campaign_id} optimized"}

@router.get("/insights/{campaign_id}")
async def get_insights(campaign_id: str, req: Request, user: dict = Depends(get_current_user)):
    """Get campaign insights."""
    return {"status": "success", "campaign_id": campaign_id, "insights": {}}

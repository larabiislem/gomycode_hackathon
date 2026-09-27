"""Creative routes."""
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from brandforge.api.middleware.auth import get_current_user

router = APIRouter(prefix="/api/creative", tags=["Creative"])

class BriefRequest(BaseModel):
    campaign_name: str
    objectives: str

class ImageGenerateRequest(BaseModel):
    prompt: str
    aspect_ratio: str = "1:1"

@router.post("/brief")
async def generate_brief(request: BriefRequest, req: Request, user: dict = Depends(get_current_user)):
    """Generate creative brief via Creative Director."""
    return {"status": "success", "brief": f"Creative brief for {request.campaign_name}"}

@router.post("/generate-image")
async def generate_image(request: ImageGenerateRequest, req: Request, user: dict = Depends(get_current_user)):
    """Generate image via Image Generator."""
    return {"status": "success", "image_url": "https://example.com/generated-image.png"}

@router.get("/assets")
async def list_assets(req: Request, user: dict = Depends(get_current_user)):
    """List generated assets."""
    return {"status": "success", "assets": []}

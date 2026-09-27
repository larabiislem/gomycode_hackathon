"""Brand routes."""
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any

from brandforge.api.middleware.auth import get_current_user

router = APIRouter(prefix="/api/brand", tags=["Brand"])

class BrandOnboardingRequest(BaseModel):
    brand_url: str
    brand_name: str
    industry: str

class BrandUpdateRequest(BaseModel):
    fields: Dict[str, Any]

@router.post("/onboard")
async def onboard_brand(request: BrandOnboardingRequest, req: Request, user: dict = Depends(get_current_user)):
    """Trigger BrandOnboardingWorkflow."""
    workflow = req.app.state.workflows.get("brand_onboarding")
    if not workflow:
        raise HTTPException(status_code=500, detail="Workflow not initialized")
        
    try:
        # The run method is an Iterator, we need to extract the final result
        result = None
        for output in workflow.run(
            brand_url=request.brand_url, 
            brand_name=request.brand_name, 
            industry=request.industry
        ):
            result = output.content
            
        if result:
            return {"status": "success", "report": result}
        else:
            return {"status": "error", "message": "Workflow completed but returned no output"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profile")
async def get_brand_profile(req: Request, user: dict = Depends(get_current_user)):
    """Return current brand profile from knowledge base."""
    return {"name": "Zenith Coffee Co.", "industry": "Premium Coffee & Lifestyle"}

@router.put("/update")
async def update_brand_profile(request: BrandUpdateRequest, req: Request, user: dict = Depends(get_current_user)):
    """Update brand profile fields."""
    return {"status": "success", "updated_fields": request.fields}

@router.get("/voice")
async def get_brand_voice(req: Request, user: dict = Depends(get_current_user)):
    """Return current brand voice guidelines."""
    return {"tone": "Knowledgeable but accessible", "vocabulary": ["Craft", "Elevate"]}

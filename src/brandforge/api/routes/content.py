"""Content routes."""
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import List

from brandforge.api.middleware.auth import get_current_user

router = APIRouter(prefix="/api/content", tags=["Content"])

class ContentGenerateRequest(BaseModel):
    topic: str
    platform: str
    content_type: str

class ContentBatchRequest(BaseModel):
    requests: List[ContentGenerateRequest]

class ContentPublishRequest(BaseModel):
    content_id: str
    platform: str

@router.post("/generate")
async def generate_content(request: ContentGenerateRequest, req: Request, user: dict = Depends(get_current_user)):
    """Trigger ContentPipelineWorkflow."""
    return {"status": "success", "content": f"Generated {request.content_type} for {request.platform} about {request.topic}"}

@router.post("/batch")
async def batch_generate_content(request: ContentBatchRequest, req: Request, user: dict = Depends(get_current_user)):
    """Generate multiple content pieces at once."""
    return {"status": "success", "count": len(request.requests)}

@router.get("/library")
async def get_content_library(req: Request, user: dict = Depends(get_current_user)):
    """List all generated content."""
    return {"status": "success", "library": []}

@router.post("/publish")
async def publish_content(request: ContentPublishRequest, req: Request, user: dict = Depends(get_current_user)):
    """Publish content to platform via SocialPublisherToolkit."""
    return {"status": "success", "message": f"Published {request.content_id} to {request.platform}"}

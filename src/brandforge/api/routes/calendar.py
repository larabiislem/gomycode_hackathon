"""Calendar routes."""
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from brandforge.api.middleware.auth import get_current_user

router = APIRouter(prefix="/api/calendar", tags=["Calendar"])

class RescheduleRequest(BaseModel):
    entry_id: str
    new_date: str

@router.post("/generate")
async def generate_calendar(req: Request, user: dict = Depends(get_current_user)):
    """Generate content calendar via Content Planner."""
    return {"status": "success", "message": "Calendar generated"}

@router.get("/weekly")
async def get_weekly_calendar(req: Request, user: dict = Depends(get_current_user)):
    """Get this week's calendar."""
    return {"status": "success", "calendar": {}}

@router.get("/monthly")
async def get_monthly_calendar(req: Request, user: dict = Depends(get_current_user)):
    """Get this month's calendar."""
    return {"status": "success", "calendar": {}}

@router.put("/reschedule")
async def reschedule_entry(request: RescheduleRequest, req: Request, user: dict = Depends(get_current_user)):
    """Reschedule a calendar entry."""
    return {"status": "success", "message": f"Rescheduled {request.entry_id} to {request.new_date}"}

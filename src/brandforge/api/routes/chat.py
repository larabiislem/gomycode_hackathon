"""Chat routes."""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json

from brandforge.api.middleware.auth import get_current_user

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

@router.post("/message")
async def chat_message(request: ChatMessage, req: Request, user: dict = Depends(get_current_user)):
    """
    Chat with CMO agent (the executive team).
    Uses SSE for streaming.
    """
    executive_team = req.app.state.executive_team if hasattr(req.app.state, "executive_team") else None
    
    async def generate_response():
        if executive_team:
            try:
                # Assuming arun returns an async generator for stream=True in AGNO
                async for chunk in executive_team.arun(request.message, stream=True):
                    content = chunk.content if hasattr(chunk, "content") else str(chunk)
                    yield f"data: {json.dumps({'content': content})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        else:
            # Fallback for hackathon testing without real agent
            words = f"Echoing from CMO: {request.message}".split()
            for word in words:
                yield f"data: {json.dumps({'content': word + ' '})}\n\n"
        
        yield "data: [DONE]\n\n"
        
    return StreamingResponse(generate_response(), media_type="text/event-stream")

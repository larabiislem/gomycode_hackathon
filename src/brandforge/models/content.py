from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from brandforge.config.constants import Platform, ContentType, PostStatus

class ContentIdea(BaseModel):
    title: str = Field(description="Title of the idea")
    description: str = Field(description="Detailed description")
    pillar: str = Field(description="Associated content pillar")
    platform: Platform = Field(description="Target platform")
    content_type: ContentType = Field(description="Format of the content")
    inspiration_source: Optional[str] = Field(None, description="Where the idea came from")
    trending_score: float = Field(ge=0.0, le=1.0, description="How trendy this topic is (0-1)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "5 Ways to Upcycle",
                "description": "A carousel showing easy upcycling projects.",
                "pillar": "Sustainability Education",
                "platform": "INSTAGRAM",
                "content_type": "CAROUSEL",
                "inspiration_source": "Recent viral TikTok trend",
                "trending_score": 0.85
            }
        }
    }

class SocialPost(BaseModel):
    id: str = Field(description="Unique identifier for the post")
    brand_id: str = Field(description="Associated brand ID")
    platform: Platform = Field(description="Target platform")
    content_type: ContentType = Field(description="Format of the content")
    caption: str = Field(description="Post caption text")
    hashtags: List[str] = Field(default_factory=list, description="List of hashtags")
    cta: str = Field(description="Call to action text")
    hook: str = Field(description="Opening hook to grab attention")
    media_urls: List[str] = Field(default_factory=list, description="URLs to media assets")
    scheduled_at: Optional[datetime] = Field(None, description="When the post is scheduled")
    published_at: Optional[datetime] = Field(None, description="When the post was published")
    status: PostStatus = Field(description="Current status of the post")
    pillar: str = Field(description="Associated content pillar")
    campaign_id: Optional[str] = Field(None, description="Optional associated campaign ID")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "post_123",
                "brand_id": "brand_123",
                "platform": "INSTAGRAM",
                "content_type": "REEL",
                "caption": "Did you know 85% of textiles end up in dumps?",
                "hashtags": ["#SustainableFashion", "#EcoFriendly"],
                "cta": "Read our latest blog!",
                "hook": "Stop scrolling if you care about the planet.",
                "media_urls": ["https://assets.example.com/reel1.mp4"],
                "status": "DRAFT",
                "pillar": "Educational"
            }
        }
    }

class CalendarEntry(BaseModel):
    date: datetime = Field(description="The date of the entry")
    time_slot: str = Field(description="Time slot (e.g., 'Morning', '14:00')")
    platform: Platform = Field(description="Platform for the post")
    content_type: ContentType = Field(description="Format of the content")
    topic: str = Field(description="General topic")
    pillar: str = Field(description="Associated content pillar")
    assigned_post_id: Optional[str] = Field(None, description="Linked post ID if drafted")
    status: str = Field(description="Status of the calendar slot")
    notes: Optional[str] = Field(None, description="Internal notes")

    model_config = {
        "json_schema_extra": {
            "example": {
                "date": "2023-10-01T00:00:00Z",
                "time_slot": "Morning",
                "platform": "INSTAGRAM",
                "content_type": "POST",
                "topic": "New Collection Teaser",
                "pillar": "Promotional",
                "status": "Planned"
            }
        }
    }

class ContentCalendar(BaseModel):
    brand_id: str = Field(description="Brand ID")
    week_start: datetime = Field(description="Start date of the week")
    week_end: datetime = Field(description="End date of the week")
    entries: List[CalendarEntry] = Field(default_factory=list, description="Calendar entries")
    strategy_alignment_notes: Optional[str] = Field(None, description="Notes on how this aligns with strategy")

    model_config = {
        "json_schema_extra": {
            "example": {
                "brand_id": "brand_123",
                "week_start": "2023-10-01T00:00:00Z",
                "week_end": "2023-10-07T23:59:59Z",
                "entries": [],
                "strategy_alignment_notes": "Focusing heavily on user-generated content this week."
            }
        }
    }

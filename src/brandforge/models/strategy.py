from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from brandforge.config.constants import Platform, CampaignObjectiveType
from brandforge.models.brand import TargetAudience

class ContentPillar(BaseModel):
    name: str = Field(description="Name of the content pillar")
    description: str = Field(description="Description of what this pillar covers")
    content_ratio: float = Field(description="Target percentage of content for this pillar (0.0 to 1.0)")
    example_topics: List[str] = Field(default_factory=list, description="List of example topics under this pillar")
    target_audience_segments: List[str] = Field(default_factory=list, description="Audience segments this pillar targets")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Sustainability Education",
                "description": "Educating the audience on sustainable practices.",
                "content_ratio": 0.4,
                "example_topics": ["How to recycle", "Impact of fast fashion"],
                "target_audience_segments": ["Young Professionals"]
            }
        }
    }

class CompetitorInsight(BaseModel):
    name: str = Field(description="Competitor name")
    website: Optional[str] = Field(None, description="Competitor website")
    social_profiles: Dict[Platform, str] = Field(default_factory=dict, description="Competitor social profiles")
    strengths: List[str] = Field(default_factory=list, description="Competitor strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Competitor weaknesses")
    content_frequency: str = Field(description="How often the competitor posts")
    engagement_rate: float = Field(description="Estimated engagement rate")
    key_themes: List[str] = Field(default_factory=list, description="Common themes in competitor content")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "FastFashionCo",
                "website": "https://fastfashionco.example",
                "social_profiles": {"INSTAGRAM": "https://instagram.com/fastfashionco"},
                "strengths": ["High posting frequency", "Large following"],
                "weaknesses": ["Low engagement", "Generic content"],
                "content_frequency": "Daily",
                "engagement_rate": 0.015,
                "key_themes": ["Sales", "New arrivals"]
            }
        }
    }

class CampaignObjective(BaseModel):
    name: str = Field(description="Name of the objective")
    type: CampaignObjectiveType = Field(description="Type of campaign objective")
    kpis: List[str] = Field(default_factory=list, description="Key Performance Indicators")
    target_metrics: Dict[str, float] = Field(default_factory=dict, description="Target metrics values")
    timeline_days: int = Field(description="Expected duration of the campaign in days")
    budget: Optional[float] = Field(None, description="Allocated budget")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Q3 Brand Awareness",
                "type": "AWARENESS",
                "kpis": ["Reach", "Impressions"],
                "target_metrics": {"reach": 100000.0},
                "timeline_days": 30,
                "budget": 5000.0
            }
        }
    }

class MarketingStrategy(BaseModel):
    brand_id: str = Field(description="The brand this strategy belongs to")
    pillars: List[ContentPillar] = Field(default_factory=list, description="Content pillars")
    target_audiences: List[TargetAudience] = Field(default_factory=list, description="Target audience segments")
    campaigns: List[CampaignObjective] = Field(default_factory=list, description="Planned campaigns")
    competitors: List[CompetitorInsight] = Field(default_factory=list, description="Competitor analysis")
    content_mix: Dict[str, float] = Field(default_factory=dict, description="Content mix distribution")
    posting_frequency: Dict[Platform, int] = Field(default_factory=dict, description="Target posts per week by platform")
    key_messages: List[str] = Field(default_factory=list, description="Core key messages to deliver")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    model_config = {
        "json_schema_extra": {
            "example": {
                "brand_id": "brand_123",
                "pillars": [],
                "target_audiences": [],
                "campaigns": [],
                "competitors": [],
                "content_mix": {"EDUCATIONAL": 0.4},
                "posting_frequency": {"INSTAGRAM": 5},
                "key_messages": ["Sustainability is a choice."],
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        }
    }

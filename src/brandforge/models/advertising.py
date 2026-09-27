from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from brandforge.config.constants import Platform, CampaignObjectiveType, AdStatus

class AdTargeting(BaseModel):
    age_min: int = Field(default=18, description="Minimum target age")
    age_max: int = Field(default=65, description="Maximum target age")
    genders: List[str] = Field(default_factory=lambda: ["ALL"], description="Target genders")
    locations: List[str] = Field(default_factory=list, description="Target geographical locations")
    interests: List[str] = Field(default_factory=list, description="Target interests")
    behaviors: List[str] = Field(default_factory=list, description="Target behaviors")
    custom_audiences: List[str] = Field(default_factory=list, description="IDs of custom audiences to include")
    lookalike_audiences: List[str] = Field(default_factory=list, description="IDs of lookalike audiences to include")

    model_config = {
        "json_schema_extra": {
            "example": {
                "age_min": 18,
                "age_max": 35,
                "genders": ["ALL"],
                "locations": ["US", "UK", "Canada"],
                "interests": ["Sustainable Living", "Eco-friendly products"],
                "behaviors": ["Engaged Shoppers"]
            }
        }
    }

class AdCreative(BaseModel):
    headline: str = Field(description="Ad headline")
    primary_text: str = Field(description="Main body text of the ad")
    description: Optional[str] = Field(None, description="Sub-description or link description")
    cta_type: str = Field(description="Call to action button type (e.g., 'LEARN_MORE')")
    image_url: Optional[str] = Field(None, description="URL of ad image")
    video_url: Optional[str] = Field(None, description="URL of ad video")
    format: str = Field(description="Format of the ad (e.g., 'SINGLE_IMAGE', 'CAROUSEL')")

    model_config = {
        "json_schema_extra": {
            "example": {
                "headline": "Upgrade Your Wardrobe Sustainably",
                "primary_text": "Our new summer collection is here. 100% organic cotton.",
                "description": "Free shipping on orders over $50.",
                "cta_type": "SHOP_NOW",
                "image_url": "https://assets.example.com/ad1.jpg",
                "format": "SINGLE_IMAGE"
            }
        }
    }

class AdSet(BaseModel):
    name: str = Field(description="Name of the ad set")
    targeting: AdTargeting = Field(description="Targeting criteria")
    budget_amount: float = Field(description="Budget allocated to this ad set")
    budget_type: str = Field(description="'daily' or 'lifetime'")
    bid_strategy: str = Field(description="Bidding strategy (e.g., 'LOWEST_COST')")
    placement: List[Platform] = Field(default_factory=list, description="Platforms to display ads on")
    schedule_start: datetime = Field(description="Start time of ad set")
    schedule_end: Optional[datetime] = Field(None, description="End time of ad set")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "US/UK Millennials - Engaged Shoppers",
                "targeting": {
                    "age_min": 25,
                    "age_max": 34,
                    "genders": ["ALL"],
                    "locations": ["US", "UK"],
                    "interests": ["Sustainable Fashion"],
                    "behaviors": []
                },
                "budget_amount": 50.0,
                "budget_type": "daily",
                "bid_strategy": "LOWEST_COST",
                "placement": ["INSTAGRAM", "FACEBOOK"],
                "schedule_start": "2023-10-01T00:00:00Z"
            }
        }
    }

class AdCampaign(BaseModel):
    id: str = Field(description="Campaign ID")
    brand_id: str = Field(description="Associated brand ID")
    name: str = Field(description="Name of the campaign")
    objective: CampaignObjectiveType = Field(description="Campaign objective")
    status: AdStatus = Field(description="Current status of the campaign")
    ad_sets: List[AdSet] = Field(default_factory=list, description="List of ad sets in campaign")
    creatives: List[AdCreative] = Field(default_factory=list, description="List of creatives used")
    total_budget: float = Field(description="Total campaign budget")
    spent: float = Field(default=0.0, description="Amount spent so far")
    results: Dict[str, float] = Field(default_factory=dict, description="Key metrics achieved (e.g., conversions, clicks)")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "campaign_123",
                "brand_id": "brand_123",
                "name": "Summer Collection Launch",
                "objective": "CONVERSION",
                "status": "ACTIVE",
                "ad_sets": [],
                "creatives": [],
                "total_budget": 5000.0,
                "spent": 1500.50,
                "results": {"purchases": 45, "cost_per_purchase": 33.34}
            }
        }
    }

class BudgetAllocation(BaseModel):
    campaign_id: str = Field(description="Associated campaign ID")
    total_budget: float = Field(description="Total budget available")
    daily_budget: float = Field(description="Recommended daily budget")
    platform_split: Dict[Platform, float] = Field(default_factory=dict, description="Budget percentage split by platform")
    phase_budgets: Dict[str, float] = Field(default_factory=dict, description="Budget allocation by campaign phase")

    model_config = {
        "json_schema_extra": {
            "example": {
                "campaign_id": "campaign_123",
                "total_budget": 5000.0,
                "daily_budget": 166.67,
                "platform_split": {"INSTAGRAM": 0.7, "FACEBOOK": 0.3},
                "phase_budgets": {"testing": 500.0, "scaling": 4000.0, "retargeting": 500.0}
            }
        }
    }

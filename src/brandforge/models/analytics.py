from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from brandforge.config.constants import Platform

class EngagementData(BaseModel):
    likes: int = Field(default=0, description="Number of likes")
    comments: int = Field(default=0, description="Number of comments")
    shares: int = Field(default=0, description="Number of shares")
    saves: int = Field(default=0, description="Number of saves")
    clicks: int = Field(default=0, description="Number of clicks")
    impressions: int = Field(default=0, description="Total impressions")
    reach: int = Field(default=0, description="Total reach")
    engagement_rate: float = Field(default=0.0, description="Calculated engagement rate")
    platform: Platform = Field(description="Platform the data belongs to")

    model_config = {
        "json_schema_extra": {
            "example": {
                "likes": 150,
                "comments": 20,
                "shares": 5,
                "saves": 10,
                "clicks": 50,
                "impressions": 2000,
                "reach": 1500,
                "engagement_rate": 0.05,
                "platform": "INSTAGRAM"
            }
        }
    }

class ContentScore(BaseModel):
    post_id: str = Field(description="Associated post ID")
    overall_score: float = Field(ge=0.0, le=100.0, description="Overall performance score (0-100)")
    engagement_score: float = Field(ge=0.0, le=100.0, description="Score based on engagement")
    reach_score: float = Field(ge=0.0, le=100.0, description="Score based on reach")
    conversion_score: float = Field(ge=0.0, le=100.0, description="Score based on conversions")
    virality_score: float = Field(ge=0.0, le=100.0, description="Probability/measure of virality")
    recommendations: List[str] = Field(default_factory=list, description="Actionable recommendations")

    model_config = {
        "json_schema_extra": {
            "example": {
                "post_id": "post_123",
                "overall_score": 85.5,
                "engagement_score": 90.0,
                "reach_score": 80.0,
                "conversion_score": 75.0,
                "virality_score": 60.0,
                "recommendations": ["Use more trending hashtags", "Post 1 hour earlier"]
            }
        }
    }

class KPIMetrics(BaseModel):
    period_start: datetime = Field(description="Start of the reporting period")
    period_end: datetime = Field(description="End of the reporting period")
    total_posts: int = Field(description="Total posts in period")
    total_reach: int = Field(description="Total reach across all posts")
    total_engagement: int = Field(description="Total engagement interactions")
    avg_engagement_rate: float = Field(description="Average engagement rate")
    follower_growth: int = Field(description="Net new followers")
    top_performing_posts: List[str] = Field(default_factory=list, description="IDs of top posts")
    worst_performing_posts: List[str] = Field(default_factory=list, description="IDs of worst posts")
    platform_breakdown: Dict[Platform, Dict[str, float]] = Field(default_factory=dict, description="Metrics split by platform")

    model_config = {
        "json_schema_extra": {
            "example": {
                "period_start": "2023-09-01T00:00:00Z",
                "period_end": "2023-09-30T23:59:59Z",
                "total_posts": 20,
                "total_reach": 50000,
                "total_engagement": 2500,
                "avg_engagement_rate": 0.05,
                "follower_growth": 150,
                "top_performing_posts": ["post_1", "post_2"],
                "worst_performing_posts": ["post_19"],
                "platform_breakdown": {
                    "INSTAGRAM": {"reach": 30000, "engagement": 1800}
                }
            }
        }
    }

class PerformanceReport(BaseModel):
    brand_id: str = Field(description="Brand ID")
    report_type: str = Field(description="'weekly' or 'monthly'")
    period: str = Field(description="String describing the period (e.g., 'September 2023')")
    kpis: KPIMetrics = Field(description="Key metrics for the period")
    insights: List[str] = Field(default_factory=list, description="AI-generated insights")
    recommendations: List[str] = Field(default_factory=list, description="Actionable advice for next period")
    strategy_adjustments: List[str] = Field(default_factory=list, description="Suggested changes to strategy")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="When the report was generated")

    model_config = {
        "json_schema_extra": {
            "example": {
                "brand_id": "brand_123",
                "report_type": "monthly",
                "period": "September 2023",
                "kpis": {
                    "period_start": "2023-09-01T00:00:00Z",
                    "period_end": "2023-09-30T23:59:59Z",
                    "total_posts": 20,
                    "total_reach": 50000,
                    "total_engagement": 2500,
                    "avg_engagement_rate": 0.05,
                    "follower_growth": 150,
                    "top_performing_posts": [],
                    "worst_performing_posts": [],
                    "platform_breakdown": {}
                },
                "insights": ["Reels generated 60% of reach.", "Educational content had the highest save rate."],
                "recommendations": ["Increase Reel frequency to 2x per week.", "Test new educational carousel formats."],
                "strategy_adjustments": ["Shift 10% of content mix to Educational."]
            }
        }
    }

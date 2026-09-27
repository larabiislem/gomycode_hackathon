from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from brandforge.config.constants import Tone, Platform

class BrandProfile(BaseModel):
    name: str = Field(description="The name of the brand")
    industry: str = Field(description="The industry the brand operates in")
    description: str = Field(description="A brief description of the brand")
    website: Optional[str] = Field(None, description="The official website URL")
    social_profiles: Dict[Platform, str] = Field(default_factory=dict, description="Map of platforms to profile URLs")
    founding_year: Optional[int] = Field(None, description="The year the brand was founded")
    unique_selling_points: List[str] = Field(default_factory=list, description="List of unique selling propositions")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "EcoWear",
                "industry": "Sustainable Fashion",
                "description": "Eco-friendly clothing for the modern explorer.",
                "website": "https://ecowear.example.com",
                "social_profiles": {"INSTAGRAM": "https://instagram.com/ecowear"},
                "founding_year": 2020,
                "unique_selling_points": ["100% organic cotton", "Fair trade certified"]
            }
        }
    }

class BrandIdentity(BaseModel):
    brand_id: str = Field(description="The ID of the associated brand")
    mission: str = Field(description="The brand's mission statement")
    vision: str = Field(description="The brand's vision statement")
    values: List[str] = Field(default_factory=list, description="Core values of the brand")
    personality_traits: List[str] = Field(default_factory=list, description="Personality traits of the brand")
    brand_archetype: str = Field(description="The archetype that best represents the brand")

    model_config = {
        "json_schema_extra": {
            "example": {
                "brand_id": "brand_123",
                "mission": "To make sustainable fashion accessible.",
                "vision": "A world where every garment is earth-friendly.",
                "values": ["Sustainability", "Transparency"],
                "personality_traits": ["Earthy", "Modern", "Approachable"],
                "brand_archetype": "The Explorer"
            }
        }
    }

class TargetAudience(BaseModel):
    segment_name: str = Field(description="Name of the audience segment")
    demographics: Dict[str, str] = Field(description="Demographic details (e.g., age_range, gender, location, income_level)")
    psychographics: Dict[str, List[str]] = Field(description="Psychographic details (e.g., interests, pain_points, aspirations)")
    platforms: List[Platform] = Field(default_factory=list, description="Platforms where this audience is most active")

    model_config = {
        "json_schema_extra": {
            "example": {
                "segment_name": "Young Professionals",
                "demographics": {"age_range": "25-34", "location": "Urban areas"},
                "psychographics": {"interests": ["Sustainability", "Outdoors"], "pain_points": ["Fast fashion waste"]},
                "platforms": ["INSTAGRAM", "TIKTOK"]
            }
        }
    }

class BrandVoice(BaseModel):
    tone: Tone = Field(description="The primary tone of voice")
    communication_style: str = Field(description="How the brand communicates (e.g., direct, storytelling)")
    dos: List[str] = Field(default_factory=list, description="Things to do when writing for this brand")
    donts: List[str] = Field(default_factory=list, description="Things to avoid when writing for this brand")
    sample_phrases: List[str] = Field(default_factory=list, description="Examples of phrases commonly used")
    emoji_usage: bool = Field(description="Whether the brand uses emojis frequently")
    hashtag_style: str = Field(description="How the brand uses hashtags (e.g., minimalist, branded)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "tone": "CASUAL",
                "communication_style": "Storytelling and engaging",
                "dos": ["Use inclusive language", "Highlight sustainability"],
                "donts": ["Use overly corporate jargon"],
                "sample_phrases": ["Join the movement", "Earth-first"],
                "emoji_usage": True,
                "hashtag_style": "3-5 highly relevant hashtags at the end"
            }
        }
    }

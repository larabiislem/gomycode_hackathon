from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from brandforge.config.constants import Platform, ContentType, Tone

class VisualConcept(BaseModel):
    style: str = Field(description="Overall visual style (e.g., minimalist, vibrant)")
    color_palette: List[str] = Field(default_factory=list, description="List of hex colors")
    mood: str = Field(description="The mood the visual should evoke")
    composition_notes: Optional[str] = Field(None, description="Notes on visual composition")
    reference_urls: List[str] = Field(default_factory=list, description="Inspiration images/links")

    model_config = {
        "json_schema_extra": {
            "example": {
                "style": "Minimalist and clean",
                "color_palette": ["#FFFFFF", "#000000", "#4CAF50"],
                "mood": "Calm and professional",
                "reference_urls": ["https://pinterest.com/pin/123"]
            }
        }
    }

class DesignSpec(BaseModel):
    format: str = Field(description="Format dimensions (e.g., '1080x1080')")
    platform: Platform = Field(description="Target platform")
    content_type: ContentType = Field(description="Content type")
    aspect_ratio: str = Field(description="Aspect ratio (e.g., '1:1')")
    file_format: str = Field(description="Required file format (e.g., 'mp4', 'png')")
    max_file_size_mb: Optional[float] = Field(None, description="Max file size in MB")

    model_config = {
        "json_schema_extra": {
            "example": {
                "format": "1080x1080",
                "platform": "INSTAGRAM",
                "content_type": "POST",
                "aspect_ratio": "1:1",
                "file_format": "png",
                "max_file_size_mb": 10.0
            }
        }
    }

class CreativeBrief(BaseModel):
    id: str = Field(description="Unique brief ID")
    brand_id: str = Field(description="Associated brand ID")
    title: str = Field(description="Title of the brief")
    objective: str = Field(description="Main objective of the creative")
    target_audience: str = Field(description="Target audience segment")
    key_message: str = Field(description="Core message to communicate")
    visual_concept: VisualConcept = Field(description="Visual direction")
    design_spec: DesignSpec = Field(description="Technical specifications")
    copy_text: Optional[str] = Field(None, description="Proposed copy/text on image")
    cta: Optional[str] = Field(None, description="Call to action")
    tone: Tone = Field(description="Tone of the creative")
    references: List[str] = Field(default_factory=list, description="External references")
    deadline: Optional[datetime] = Field(None, description="When the creative is needed")
    notes: Optional[str] = Field(None, description="Additional notes")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "brief_123",
                "brand_id": "brand_123",
                "title": "Summer Sale Banner",
                "objective": "Drive clicks to website",
                "target_audience": "Millennials",
                "key_message": "Up to 50% off summer essentials",
                "visual_concept": {
                    "style": "Vibrant and summery",
                    "color_palette": ["#FFEB3B", "#FF9800"],
                    "mood": "Excited",
                    "reference_urls": []
                },
                "design_spec": {
                    "format": "1080x1080",
                    "platform": "INSTAGRAM",
                    "content_type": "POST",
                    "aspect_ratio": "1:1",
                    "file_format": "jpg",
                    "max_file_size_mb": 5.0
                },
                "tone": "CASUAL"
            }
        }
    }

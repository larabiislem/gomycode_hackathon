"""Main FastAPI application for BrandForge AI.

The central FastAPI server that initializes the database, knowledge base,
multi-agent executive team, and exposes all REST API endpoints.
"""

import json
import logging
from contextlib import asynccontextmanager
from datetime import timedelta
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

# Import local modules
from brandforge.db.database import init_database, get_db
from brandforge.knowledge.brand_kb import create_brand_knowledge_base, ingest_seed_data
from brandforge.api.middleware.auth import AuthRequest, create_access_token, MOCK_USERS, ACCESS_TOKEN_EXPIRE_MINUTES

# Import routers
from brandforge.api.routes import brand, strategy, content, calendar, creative, analytics, ads, chat

logger = logging.getLogger("brandforge")


def _load_brand_context() -> dict:
    """Load the sample brand context from seed data."""
    seed_path = Path(__file__).parent.parent / "knowledge" / "seed_data" / "sample_brand.json"
    if seed_path.exists():
        with open(seed_path, "r") as f:
            return json.load(f)
    return {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for FastAPI."""
    # Startup: Initialize DB, knowledge base, create teams
    logger.info("🚀 Starting BrandForge AI platform...")

    # Initialize Database
    init_database()
    db = get_db()
    app.state.db = db
    logger.info("✅ Database initialized")

    # Initialize Knowledge Base
    kb = create_brand_knowledge_base()
    try:
        ingest_seed_data(kb)
        logger.info("✅ Knowledge base initialized with seed data")
    except Exception as e:
        logger.warning(f"⚠️ Seed data ingestion skipped (may need OPENAI_API_KEY): {e}")
    app.state.knowledge = kb

    # Load brand context
    brand_context = _load_brand_context()
    app.state.brand_context = brand_context

    # Initialize Executive Team (CMO + all sub-teams)
    try:
        from brandforge.teams.executive_team import create_executive_team
        app.state.executive_team = create_executive_team(
            knowledge=kb,
            db=db,
            brand_context=brand_context,
        )
        logger.info("✅ Executive Team initialized (CMO + 3 sub-teams + 11 agents)")
    except Exception as e:
        logger.warning(f"⚠️ Executive Team init skipped (may need API keys): {e}")
        app.state.executive_team = None

    # Initialize Workflows
    app.state.workflows = {}
    
    try:
        from brandforge.workflows.brand_onboarding import BrandOnboardingWorkflow
        app.state.workflows["brand_onboarding"] = BrandOnboardingWorkflow(knowledge=kb, db=db)
        logger.info("✅ BrandOnboardingWorkflow initialized")
    except Exception as e:
        logger.warning(f"⚠️ BrandOnboardingWorkflow init skipped: {e}")

    try:
        from brandforge.workflows.content_pipeline import ContentPipelineWorkflow
        app.state.workflows["content_pipeline"] = ContentPipelineWorkflow(knowledge=kb, db=db)
        logger.info("✅ ContentPipelineWorkflow initialized")
    except Exception as e:
        logger.warning(f"⚠️ ContentPipelineWorkflow init skipped: {e}")

    try:
        from brandforge.workflows.campaign_launch import CampaignLaunchWorkflow
        app.state.workflows["campaign_launch"] = CampaignLaunchWorkflow(knowledge=kb, db=db)
        logger.info("✅ CampaignLaunchWorkflow initialized")
    except Exception as e:
        logger.warning(f"⚠️ CampaignLaunchWorkflow init skipped: {e}")

    try:
        from brandforge.workflows.performance_review import PerformanceReviewWorkflow
        app.state.workflows["performance_review"] = PerformanceReviewWorkflow(knowledge=kb, db=db)
        logger.info("✅ PerformanceReviewWorkflow initialized")
    except Exception as e:
        logger.warning(f"⚠️ PerformanceReviewWorkflow init skipped: {e}")

    logger.info(f"✅ Total workflows initialized: {len(app.state.workflows)}")

    logger.info("🎯 BrandForge AI is ready!")

    yield

    # Shutdown: cleanup
    logger.info("👋 Shutting down BrandForge AI platform...")

app = FastAPI(
    title="BrandForge AI",
    description="AI-Powered Brand Growth & Marketing Automation Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication token endpoint
@app.post("/api/auth/token", tags=["Auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = MOCK_USERS.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Include all routers
app.include_router(brand.router)
app.include_router(strategy.router)
app.include_router(content.router)
app.include_router(calendar.router)
app.include_router(creative.router)
app.include_router(analytics.router)
app.include_router(ads.router)
app.include_router(chat.router)

@app.get("/health", tags=["System"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "platform": "BrandForge AI", "version": "1.0.0"}

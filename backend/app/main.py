"""FastAPI application entry point.

Creates the FastAPI app, configures CORS middleware,
and includes all routers.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router
from app.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown events."""
    settings = get_settings()
    logger.info(f"🚀 Starting {settings.app_name}")
    logger.info(f"📡 Gemini model: {settings.gemini_model}")

    api_key = settings.google_api_key
    if api_key and api_key != "your_google_api_key_here":
        logger.info("✅ Google API key configured")
    else:
        logger.warning(
            "⚠️  No Google API key configured — running with mock responses. "
            "Set GOOGLE_API_KEY in backend/.env to enable AI features."
        )

    yield

    logger.info("👋 Shutting down")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description=(
            "AI-powered career counselor for women restarting their careers. "
            "Provides career analysis, employability scoring, personalized roadmaps, "
            "and AI coaching chat."
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False if "*" in settings.cors_origins else True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(router, prefix=settings.api_prefix)

    # Health check
    @app.get("/")
    async def health_check():
        return {
            "status": "healthy",
            "app": settings.app_name,
            "version": "1.0.0",
        }

    @app.get("/catalogs")
    async def get_catalogs():
        """Return skill and interest catalogs for the frontend."""
        from app.services.career_analyzer import (
            EDUCATION_LEVELS,
            INTERESTS_CATALOG,
            SKILLS_CATALOG,
        )

        return {
            "skills": SKILLS_CATALOG,
            "interests": INTERESTS_CATALOG,
            "education_levels": EDUCATION_LEVELS,
        }

    return app


app = create_app()

"""API route handlers for the Career Counselor."""

import logging

from fastapi import APIRouter, HTTPException

from app.schemas.requests import ChatRequest, RoadmapRequest, UserProfile
from app.schemas.responses import (
    AnalysisResult,
    ChatResponse,
    RoadmapResult,
    ScoreResult,
)
from app.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_profile(profile: UserProfile):
    """Analyze a user's profile and return career recommendations.

    Returns 3 career cards with match percentages, a skill gap analysis,
    and an overall summary.
    """
    try:
        result = await gemini_service.analyze_profile(profile)
        return AnalysisResult(**result)
    except Exception as e:
        logger.error(f"Analysis endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze profile: {str(e)}",
        )


@router.post("/score", response_model=ScoreResult)
async def get_score(profile: UserProfile):
    """Calculate an employability score for the user.

    Returns an overall score (0-100), breakdown by category,
    recommendations, and a verdict.
    """
    try:
        result = await gemini_service.calculate_score(profile)
        return ScoreResult(**result)
    except Exception as e:
        logger.error(f"Score endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate score: {str(e)}",
        )


@router.post("/roadmap", response_model=RoadmapResult)
async def get_roadmap(request: RoadmapRequest):
    """Generate a 30/60/90 day career roadmap.

    Takes the user profile and their selected career path,
    returns a structured action plan with tasks, resources, and milestones.
    """
    try:
        result = await gemini_service.generate_roadmap(
            request.profile, request.selected_career
        )
        return RoadmapResult(**result)
    except Exception as e:
        logger.error(f"Roadmap endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate roadmap: {str(e)}",
        )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Career coaching chat endpoint.

    Accepts a message with conversation history and optional user profile
    for personalized responses.
    """
    try:
        result = await gemini_service.chat(
            message=request.message,
            history=request.conversation_history,
            profile=request.user_profile,
        )
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Chat error: {str(e)}",
        )

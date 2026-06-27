"""Pydantic v2 request models for the Career Counselor API."""

from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """Complete user profile from the intake form."""

    name: str = Field(..., min_length=1, max_length=100, description="User's name")
    education: str = Field(
        ...,
        description="Highest education level",
        examples=["Bachelor's", "Master's", "PhD", "Bootcamp/Certification"],
    )
    previous_job: str = Field(
        ..., min_length=1, description="Most recent or most relevant job title"
    )
    career_gap_years: float = Field(
        ..., ge=0, le=30, description="Number of years away from the workforce"
    )
    skills: list[str] = Field(
        ..., min_length=1, description="Current skills the user possesses"
    )
    interests: list[str] = Field(
        ..., min_length=1, description="Industries or fields of interest"
    )
    goal_role: str = Field(
        ..., min_length=1, description="Target role or career direction"
    )
    hours_per_day: int = Field(
        ..., ge=1, le=16, description="Hours available per day for upskilling"
    )
    target_months: int = Field(
        ..., ge=1, le=36, description="Target timeline in months to be job-ready"
    )


class RoadmapRequest(BaseModel):
    """Request for generating a career roadmap."""

    profile: UserProfile
    selected_career: str = Field(
        ..., description="The career path the user selected from analysis results"
    )


class ChatMessage(BaseModel):
    """A single chat message."""

    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request for the career coaching chat."""

    message: str = Field(..., min_length=1, description="User's current message")
    conversation_history: list[ChatMessage] = Field(
        default_factory=list, description="Previous messages for context"
    )
    user_profile: UserProfile | None = Field(
        default=None, description="Optional user profile for personalized advice"
    )

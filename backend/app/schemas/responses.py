"""Pydantic v2 response models for the Career Counselor API."""

from pydantic import BaseModel, Field


class CareerCard(BaseModel):
    """A single career recommendation."""

    title: str = Field(..., description="Career/role title")
    match_percentage: int = Field(
        ..., ge=0, le=100, description="How well this career matches the user"
    )
    description: str = Field(..., description="Brief description of the career path")
    required_skills: list[str] = Field(
        ..., description="Key skills needed for this career"
    )
    growth_outlook: str = Field(
        ..., description="Job market growth outlook (e.g., 'High Growth', 'Stable')"
    )
    avg_salary: str = Field(
        default="Varies", description="Average salary range"
    )


class SkillGap(BaseModel):
    """A single skill gap entry."""

    skill_name: str = Field(..., description="Name of the skill")
    category: str = Field(
        ..., description="'have' for existing skills, 'need' for required skills"
    )
    proficiency_level: str = Field(
        ...,
        description="Proficiency level: 'Beginner', 'Intermediate', 'Advanced', 'Expert'",
    )
    priority: str = Field(
        default="Medium", description="'High', 'Medium', or 'Low' priority"
    )


class AnalysisResult(BaseModel):
    """Complete career analysis response."""

    career_cards: list[CareerCard] = Field(
        ..., min_length=1, max_length=5, description="Recommended career paths"
    )
    skill_gaps: list[SkillGap] = Field(
        ..., description="Skills breakdown: have vs need"
    )
    summary: str = Field(..., description="Overall analysis summary")
    strengths: list[str] = Field(
        default_factory=list, description="Key strengths identified"
    )


class RoadmapTask(BaseModel):
    """A single task in the roadmap."""

    task: str = Field(..., description="What to do")
    resource: str = Field(..., description="Recommended resource or platform")
    milestone: str = Field(..., description="Expected outcome or milestone")


class RoadmapResult(BaseModel):
    """30/60/90 day career roadmap."""

    day_30: list[RoadmapTask] = Field(
        ..., description="Tasks for the first 30 days"
    )
    day_60: list[RoadmapTask] = Field(
        ..., description="Tasks for days 31-60"
    )
    day_90: list[RoadmapTask] = Field(
        ..., description="Tasks for days 61-90"
    )
    summary: str = Field(default="", description="Roadmap overview")


class ScoreBreakdown(BaseModel):
    """Breakdown of the employability score."""

    education_score: int = Field(..., ge=0, le=100)
    skills_score: int = Field(..., ge=0, le=100)
    experience_relevance: int = Field(..., ge=0, le=100)
    market_demand: int = Field(..., ge=0, le=100)
    gap_impact: int = Field(..., ge=0, le=100)


class ScoreResult(BaseModel):
    """Employability score response."""

    overall_score: int = Field(..., ge=0, le=100, description="Overall score 0-100")
    breakdown: ScoreBreakdown = Field(..., description="Score breakdown by category")
    recommendations: list[str] = Field(
        ..., description="Top recommendations to improve score"
    )
    verdict: str = Field(
        ...,
        description="Overall verdict: 'Ready', 'Almost There', 'Needs Work', 'Getting Started'",
    )


class ChatResponse(BaseModel):
    """Chat endpoint response."""

    reply: str = Field(..., description="AI assistant's reply")
    suggestions: list[str] = Field(
        default_factory=list,
        description="Suggested follow-up questions",
    )

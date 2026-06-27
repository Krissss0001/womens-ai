"""Google Gemini AI service layer.

Handles all interactions with the Gemini API, including prompt
construction, API calls, and response parsing.
"""

import json
import logging
import re
from typing import Any

from google import genai

from app.config import get_settings
from app.prompts.templates import (
    ANALYZE_PROMPT,
    CHAT_SYSTEM_PROMPT,
    ROADMAP_PROMPT,
    SCORE_PROMPT,
)
from app.schemas.requests import ChatMessage, UserProfile

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini AI."""

    def __init__(self):
        settings = get_settings()
        self.model_name = settings.gemini_model
        self._api_key = settings.google_api_key
        self._client = None

    @property
    def client(self) -> genai.Client:
        """Lazy-init the Gemini client."""
        if self._client is None:
            self._client = genai.Client(api_key=self._api_key)
        return self._client

    def _is_configured(self) -> bool:
        """Check if API key is set to a real value."""
        return (
            self._api_key
            and self._api_key != "your_google_api_key_here"
            and len(self._api_key) > 10
        )

    def _extract_json(self, text: str) -> dict[str, Any]:
        """Extract JSON from Gemini response, handling markdown code blocks."""
        # Remove markdown code fences if present
        cleaned = re.sub(r"```(?:json)?\s*", "", text)
        cleaned = cleaned.strip()

        # Try parsing the whole thing
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # Try to find JSON object in the text
        match = re.search(r"\{[\s\S]*\}", cleaned)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        raise ValueError(f"Could not extract valid JSON from response: {text[:200]}...")

    def _format_profile(self, profile: UserProfile) -> dict[str, str]:
        """Convert a UserProfile to template format kwargs."""
        return {
            "name": profile.name,
            "education": profile.education,
            "previous_job": profile.previous_job,
            "career_gap_years": str(profile.career_gap_years),
            "skills": ", ".join(profile.skills),
            "interests": ", ".join(profile.interests),
            "goal_role": profile.goal_role,
            "hours_per_day": str(profile.hours_per_day),
            "target_months": str(profile.target_months),
        }

    async def analyze_profile(self, profile: UserProfile) -> dict[str, Any]:
        """Analyze user profile and return career recommendations."""
        if not self._is_configured():
            return self._mock_analysis(profile)

        prompt = ANALYZE_PROMPT.format(**self._format_profile(profile))

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return self._extract_json(response.text)
        except Exception as e:
            logger.error(f"Gemini analyze error: {e}")
            return self._mock_analysis(profile)

    async def calculate_score(self, profile: UserProfile) -> dict[str, Any]:
        """Calculate employability score."""
        if not self._is_configured():
            return self._mock_score(profile)

        prompt = SCORE_PROMPT.format(**self._format_profile(profile))

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return self._extract_json(response.text)
        except Exception as e:
            logger.error(f"Gemini score error: {e}")
            return self._mock_score(profile)

    async def generate_roadmap(
        self, profile: UserProfile, selected_career: str
    ) -> dict[str, Any]:
        """Generate 30/60/90 day roadmap."""
        if not self._is_configured():
            return self._mock_roadmap(profile, selected_career)

        fmt = self._format_profile(profile)
        fmt["selected_career"] = selected_career
        prompt = ROADMAP_PROMPT.format(**fmt)

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return self._extract_json(response.text)
        except Exception as e:
            logger.error(f"Gemini roadmap error: {e}")
            return self._mock_roadmap(profile, selected_career)

    async def chat(
        self,
        message: str,
        history: list[ChatMessage],
        profile: UserProfile | None = None,
    ) -> dict[str, Any]:
        """Career coaching chat."""
        if not self._is_configured():
            return self._mock_chat(message)

        # Build profile context
        if profile:
            profile_ctx = (
                f"Name: {profile.name}, Education: {profile.education}, "
                f"Previous Job: {profile.previous_job}, "
                f"Career Gap: {profile.career_gap_years} years, "
                f"Skills: {', '.join(profile.skills)}, "
                f"Goal: {profile.goal_role}"
            )
        else:
            profile_ctx = "No profile provided yet."

        system_prompt = CHAT_SYSTEM_PROMPT.format(profile_context=profile_ctx)

        # Build conversation
        contents = [system_prompt]
        for msg in history:
            contents.append(f"{msg.role}: {msg.content}")
        contents.append(f"user: {message}")

        full_prompt = "\n\n".join(contents)

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
            )
            text = response.text

            # Extract suggestions if present
            suggestions = []
            if "SUGGESTIONS:" in text:
                parts = text.split("SUGGESTIONS:")
                text = parts[0].strip()
                try:
                    suggestions = json.loads(parts[1].strip())
                except (json.JSONDecodeError, IndexError):
                    suggestions = [
                        "What skills should I focus on?",
                        "How do I explain my career gap?",
                        "What networking strategies work best?",
                    ]

            return {"reply": text, "suggestions": suggestions}
        except Exception as e:
            logger.error(f"Gemini chat error: {e}")
            return self._mock_chat(message)

    # ─── Mock/Fallback responses (no API key) ───────────────────────

    def _mock_analysis(self, profile: UserProfile) -> dict[str, Any]:
        """Return realistic mock data when API key is not configured."""
        return {
            "career_cards": [
                {
                    "title": "Project Manager",
                    "match_percentage": 88,
                    "description": f"Your background in {profile.previous_job} provides strong "
                    f"foundational skills for project management. With your {profile.education} "
                    "education and organizational skills, this is an excellent transition path.",
                    "required_skills": [
                        "Agile/Scrum",
                        "Stakeholder Management",
                        "Risk Assessment",
                        "Budgeting",
                        "Communication",
                    ],
                    "growth_outlook": "High Growth",
                    "avg_salary": "$65,000 - $95,000",
                },
                {
                    "title": "UX Researcher",
                    "match_percentage": 76,
                    "description": "Your interpersonal skills and analytical thinking make UX research "
                    "a great fit. This field values diverse perspectives and career changers.",
                    "required_skills": [
                        "User Interviews",
                        "Data Analysis",
                        "Wireframing",
                        "A/B Testing",
                        "Empathy Mapping",
                    ],
                    "growth_outlook": "High Growth",
                    "avg_salary": "$70,000 - $110,000",
                },
                {
                    "title": "Digital Marketing Specialist",
                    "match_percentage": 72,
                    "description": "Digital marketing offers flexible work arrangements and values "
                    "creativity alongside analytical skills. Many certifications are available online.",
                    "required_skills": [
                        "SEO/SEM",
                        "Content Strategy",
                        "Google Analytics",
                        "Social Media",
                        "Email Marketing",
                    ],
                    "growth_outlook": "Stable Growth",
                    "avg_salary": "$50,000 - $80,000",
                },
            ],
            "skill_gaps": [
                *[
                    {
                        "skill_name": s,
                        "category": "have",
                        "proficiency_level": "Intermediate",
                        "priority": "Medium",
                    }
                    for s in profile.skills[:6]
                ],
                {
                    "skill_name": "Agile Methodology",
                    "category": "need",
                    "proficiency_level": "Beginner",
                    "priority": "High",
                },
                {
                    "skill_name": "Data Analytics",
                    "category": "need",
                    "proficiency_level": "Beginner",
                    "priority": "High",
                },
                {
                    "skill_name": "Digital Tools Proficiency",
                    "category": "need",
                    "proficiency_level": "Beginner",
                    "priority": "Medium",
                },
                {
                    "skill_name": "Industry Networking",
                    "category": "need",
                    "proficiency_level": "Beginner",
                    "priority": "High",
                },
                {
                    "skill_name": "Portfolio Building",
                    "category": "need",
                    "proficiency_level": "Beginner",
                    "priority": "Medium",
                },
            ],
            "summary": (
                f"Great news, {profile.name}! Based on your profile, you have a solid foundation "
                f"for re-entering the workforce. Your experience as a {profile.previous_job} and your "
                f"{profile.education} education give you transferable skills that are highly valued. "
                f"While a {profile.career_gap_years}-year gap may feel daunting, many employers now "
                "actively seek career returners for their unique perspectives and maturity."
            ),
            "strengths": [
                "Strong educational foundation",
                "Transferable professional experience",
                "Clear career direction",
                f"Commitment to {profile.hours_per_day} hours/day of development",
            ],
        }

    def _mock_score(self, profile: UserProfile) -> dict[str, Any]:
        """Return realistic mock employability score."""
        gap_penalty = max(0, 100 - int(profile.career_gap_years * 8))
        skills_score = min(100, len(profile.skills) * 12)
        education_map = {
            "High School": 50,
            "Associate's": 60,
            "Bachelor's": 75,
            "Master's": 85,
            "PhD": 90,
            "Bootcamp/Certification": 70,
        }
        edu_score = education_map.get(profile.education, 65)

        overall = int(
            edu_score * 0.20
            + skills_score * 0.25
            + 65 * 0.20
            + 70 * 0.20
            + gap_penalty * 0.15
        )

        if overall >= 80:
            verdict = "Ready"
        elif overall >= 65:
            verdict = "Almost There"
        elif overall >= 45:
            verdict = "Needs Work"
        else:
            verdict = "Getting Started"

        return {
            "overall_score": overall,
            "breakdown": {
                "education_score": edu_score,
                "skills_score": skills_score,
                "experience_relevance": 65,
                "market_demand": 70,
                "gap_impact": gap_penalty,
            },
            "recommendations": [
                f"Complete a certification in {profile.goal_role}-related skills",
                "Update your LinkedIn profile with a career narrative that frames your gap positively",
                "Join 2-3 professional communities in your target industry",
                "Build a portfolio with 2-3 projects showcasing your skills",
                f"Dedicate your {profile.hours_per_day} daily hours to structured learning",
            ],
            "verdict": verdict,
        }

    def _mock_roadmap(
        self, profile: UserProfile, selected_career: str
    ) -> dict[str, Any]:
        """Return realistic mock 30/60/90 day roadmap."""
        return {
            "day_30": [
                {
                    "task": f"Complete an introductory course on {selected_career} fundamentals",
                    "resource": "Coursera / LinkedIn Learning (free audit)",
                    "milestone": "Earn course completion certificate",
                },
                {
                    "task": "Update LinkedIn profile with career-returner narrative",
                    "resource": "LinkedIn.com — use career break feature",
                    "milestone": "Profile completeness score above 90%",
                },
                {
                    "task": "Join 3 professional communities and women-in-tech groups",
                    "resource": "LinkedIn Groups, Women Who Code, Elpha",
                    "milestone": "Active member in 3 communities",
                },
                {
                    "task": "Set up a professional portfolio website",
                    "resource": "GitHub Pages, Notion, or WordPress",
                    "milestone": "Live portfolio URL with bio and skills",
                },
            ],
            "day_60": [
                {
                    "task": f"Complete an intermediate {selected_career} skills course",
                    "resource": "Udemy, Google Career Certificates",
                    "milestone": "Intermediate certification earned",
                },
                {
                    "task": "Build 2 portfolio projects demonstrating key skills",
                    "resource": "GitHub, personal projects",
                    "milestone": "2 completed projects in portfolio",
                },
                {
                    "task": "Attend 2 virtual networking events or webinars",
                    "resource": "Eventbrite, Meetup.com",
                    "milestone": "Made 5+ new professional connections",
                },
                {
                    "task": "Start informational interviews with people in target role",
                    "resource": "LinkedIn outreach",
                    "milestone": "Completed 3 informational interviews",
                },
            ],
            "day_90": [
                {
                    "task": "Craft a tailored resume for target role",
                    "resource": "Resume templates from Indeed, TopResume",
                    "milestone": "ATS-optimized resume ready",
                },
                {
                    "task": "Practice mock interviews with common questions",
                    "resource": "Pramp.com, Interview Warmup by Google",
                    "milestone": "Completed 5 mock interviews",
                },
                {
                    "task": "Apply to 15-20 positions matching your profile",
                    "resource": "LinkedIn Jobs, Indeed, Glassdoor",
                    "milestone": "Submitted 15+ tailored applications",
                },
                {
                    "task": "Reach out to recruiters specializing in career returners",
                    "resource": "Path Forward, iRelaunch, LinkedIn Recruiters",
                    "milestone": "Connected with 3+ recruiters",
                },
            ],
            "summary": (
                f"This 90-day plan is designed to help {profile.name} transition into "
                f"{selected_career} with {profile.hours_per_day} hours/day of dedicated effort. "
                "Phase 1 builds your foundation, Phase 2 develops your skills and network, "
                "and Phase 3 launches your job search."
            ),
        }

    def _mock_chat(self, message: str) -> dict[str, Any]:
        """Return a helpful mock chat response."""
        return {
            "reply": (
                "Thank you for your question! I'm running in demo mode right now "
                "(no API key configured), but I want you to know that you're already "
                "taking a fantastic step by exploring your career options.\n\n"
                "When fully configured, I can help you with:\n"
                "- Personalized career advice based on your profile\n"
                "- Resume and interview tips\n"
                "- Skill development recommendations\n"
                "- Networking strategies\n"
                "- Confidence building for your career comeback\n\n"
                "To enable full AI-powered coaching, add your Google API key to the "
                "backend `.env` file. You can get a free key from Google AI Studio!"
            ),
            "suggestions": [
                "How do I explain my career gap in interviews?",
                "What are the best certifications for career changers?",
                "How can I build a professional network from scratch?",
            ],
        }


# Singleton instance
gemini_service = GeminiService()

"""API client — calls Gemini directly (no separate FastAPI server needed).

Falls back to mock responses if no GOOGLE_API_KEY is configured.
"""

import streamlit as st
from utils import gemini_service


def _build_profile_payload() -> dict:
    """Build the user profile dict from session state."""
    return {
        "name": st.session_state.get("user_name", "User"),
        "education": st.session_state.get("education", "Bachelor's"),
        "previous_job": st.session_state.get("previous_job", "Professional"),
        "career_gap_years": st.session_state.get("career_gap_years", 2),
        "skills": st.session_state.get("skills", ["Communication"]),
        "interests": st.session_state.get("interests", ["Technology"]),
        "goal_role": st.session_state.get("goal_role", "Professional"),
        "hours_per_day": st.session_state.get("hours_per_day", 4),
        "target_months": st.session_state.get("target_months", 6),
    }


def analyze_profile() -> dict | None:
    """Analyze career profile using Gemini AI."""
    try:
        return gemini_service.analyze_profile(_build_profile_payload())
    except Exception as e:
        st.error(f"❌ Analysis error: {str(e)}")
        return None


def get_score() -> dict | None:
    """Calculate employability score using Gemini AI."""
    try:
        return gemini_service.calculate_score(_build_profile_payload())
    except Exception as e:
        st.error(f"❌ Score error: {str(e)}")
        return None


def get_roadmap(selected_career: str) -> dict | None:
    """Generate 30/60/90 day roadmap using Gemini AI."""
    try:
        return gemini_service.generate_roadmap(_build_profile_payload(), selected_career)
    except Exception as e:
        st.error(f"❌ Roadmap error: {str(e)}")
        return None


def chat(message: str, history: list[dict], profile_data: dict | None = None) -> dict | None:
    """Career coaching chat using Gemini AI."""
    try:
        return gemini_service.chat(message, history, profile_data)
    except Exception as e:
        st.error(f"❌ Chat error: {str(e)}")
        return None

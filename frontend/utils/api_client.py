"""HTTP client for communicating with the FastAPI backend.

Wraps all API calls with error handling and user-friendly messages.
"""

import os
import requests
import streamlit as st

# Backend URL — checks environment variable, falls back to local dev URL
API_BASE_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")


def _build_profile_payload() -> dict:
    """Build the UserProfile payload from session state."""
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
    """Call /analyze endpoint."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json=_build_profile_payload(),
            timeout=60,
        )
        response.raise_for_status()
        return response.json()
    except requests.ConnectionError:
        st.error(
            "🔌 Cannot connect to the backend server. "
            "Make sure the FastAPI server is running on http://localhost:8000"
        )
        return None
    except requests.Timeout:
        st.error("⏱️ Request timed out. The AI is taking too long to respond.")
        return None
    except requests.HTTPError as e:
        st.error(f"❌ API error: {e.response.status_code} — {e.response.text}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None


def get_score() -> dict | None:
    """Call /score endpoint."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/score",
            json=_build_profile_payload(),
            timeout=60,
        )
        response.raise_for_status()
        return response.json()
    except requests.ConnectionError:
        st.error(
            "🔌 Cannot connect to the backend server. "
            "Make sure the FastAPI server is running on http://localhost:8000"
        )
        return None
    except Exception as e:
        st.error(f"❌ Error fetching score: {str(e)}")
        return None


def get_roadmap(selected_career: str) -> dict | None:
    """Call /roadmap endpoint."""
    try:
        payload = {
            "profile": _build_profile_payload(),
            "selected_career": selected_career,
        }
        response = requests.post(
            f"{API_BASE_URL}/roadmap",
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        return response.json()
    except requests.ConnectionError:
        st.error(
            "🔌 Cannot connect to the backend server. "
            "Make sure the FastAPI server is running on http://localhost:8000"
        )
        return None
    except Exception as e:
        st.error(f"❌ Error generating roadmap: {str(e)}")
        return None


def chat(message: str, history: list[dict], profile_data: dict | None = None) -> dict | None:
    """Call /chat endpoint."""
    try:
        payload = {
            "message": message,
            "conversation_history": history,
        }
        if profile_data:
            payload["user_profile"] = profile_data

        response = requests.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        return response.json()
    except requests.ConnectionError:
        st.error(
            "🔌 Cannot connect to the backend server. "
            "Make sure the FastAPI server is running on http://localhost:8000"
        )
        return None
    except Exception as e:
        st.error(f"❌ Chat error: {str(e)}")
        return None

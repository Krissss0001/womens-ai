"""Session state management for the Streamlit frontend.

Centralizes all session state initialization to prevent
KeyError and ensure consistent state across pages.
"""

import streamlit as st


def init_session_state():
    """Initialize all session state keys with defaults.

    Call this at the top of every page.
    """
    defaults = {
        # User profile data
        "user_name": "",
        "education": "",
        "previous_job": "",
        "career_gap_years": 2.0,
        "skills": [],
        "interests": [],
        "goal_role": "",
        "hours_per_day": 4,
        "target_months": 6,
        # Analysis results
        "analysis_result": None,
        "score_result": None,
        "roadmap_result": None,
        "selected_career": None,
        # Form submitted flag
        "form_submitted": False,
        # Chat history
        "chat_history": [],
        # Loading states
        "is_analyzing": False,
        "is_scoring": False,
        "is_roadmapping": False,
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

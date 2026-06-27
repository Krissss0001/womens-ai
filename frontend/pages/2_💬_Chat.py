"""
💬 Chat — AI Career Coach

Interactive chat page that maintains session context and calls
the /chat FastAPI endpoint for personalized career coaching.
"""

import streamlit as st

from utils.state import init_session_state
from utils.styles import inject_custom_css
from utils import api_client

# ─── Page Configuration ──────────────────────────────────────────
st.set_page_config(
    page_title="Chat — CareerHer",
    page_icon="💬",
    layout="wide",
)

# ─── Initialize ──────────────────────────────────────────────────
init_session_state()
st.markdown(inject_custom_css(), unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💜 CareerHer")
    st.markdown("*AI Career Coach*")
    st.divider()

    if st.session_state.form_submitted:
        st.success(f"👤 {st.session_state.user_name}")
        st.caption(f"🎯 Target: {st.session_state.goal_role}")
        st.divider()

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.divider()
    st.markdown(
        """
        **Quick Topics:**
        - Resume tips
        - Interview prep
        - Salary negotiation
        - Networking strategies
        - Skill development
        - Confidence building
        """
    )

# ─── Hero ────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-container">
        <h1>💬 Career Coach</h1>
        <p>Chat with your AI career counselor — get personalized advice,<br>
        interview tips, resume reviews, and more.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Quick Action Buttons ────────────────────────────────────────
st.markdown("**✨ Quick Start — tap a topic:**")

quick_cols = st.columns(4)
quick_prompts = [
    ("🎓 Certifications", "What certifications should I get for my target role?"),
    ("📄 Resume Tips", "Help me write a strong resume that addresses my career gap."),
    ("🎤 Interview Prep", "What are common interview questions for career returners?"),
    ("🤝 Networking", "How can I build a professional network from scratch?"),
]

for col, (label, prompt) in zip(quick_cols, quick_prompts):
    with col:
        if st.button(label, use_container_width=True, key=f"quick_{label}"):
            st.session_state.chat_history.append(
                {"role": "user", "content": prompt}
            )
            # Get AI response
            profile_data = None
            if st.session_state.form_submitted:
                profile_data = {
                    "name": st.session_state.user_name,
                    "education": st.session_state.education,
                    "previous_job": st.session_state.previous_job,
                    "career_gap_years": st.session_state.career_gap_years,
                    "skills": st.session_state.skills,
                    "interests": st.session_state.interests,
                    "goal_role": st.session_state.goal_role,
                    "hours_per_day": st.session_state.hours_per_day,
                    "target_months": st.session_state.target_months,
                }
            response = api_client.chat(
                prompt, st.session_state.chat_history[:-1], profile_data
            )
            if response:
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": response["reply"]}
                )
                if response.get("suggestions"):
                    st.session_state["_last_suggestions"] = response["suggestions"]
            st.rerun()

st.markdown("---")

# ─── Chat History ────────────────────────────────────────────────
for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]

    if role == "user":
        with st.chat_message("user", avatar="👩"):
            st.markdown(content)
    else:
        with st.chat_message("assistant", avatar="💜"):
            st.markdown(content)

# ─── Suggestions (after last assistant message) ──────────────────
suggestions = st.session_state.get("_last_suggestions", [])
if suggestions and st.session_state.chat_history:
    last_msg = st.session_state.chat_history[-1]
    if last_msg["role"] == "assistant":
        st.markdown("**💡 You might want to ask:**")
        sug_cols = st.columns(len(suggestions))
        for i, (col, sug) in enumerate(zip(sug_cols, suggestions)):
            with col:
                if st.button(
                    sug,
                    key=f"suggestion_{i}",
                    use_container_width=True,
                ):
                    st.session_state.chat_history.append(
                        {"role": "user", "content": sug}
                    )
                    profile_data = None
                    if st.session_state.form_submitted:
                        profile_data = {
                            "name": st.session_state.user_name,
                            "education": st.session_state.education,
                            "previous_job": st.session_state.previous_job,
                            "career_gap_years": st.session_state.career_gap_years,
                            "skills": st.session_state.skills,
                            "interests": st.session_state.interests,
                            "goal_role": st.session_state.goal_role,
                            "hours_per_day": st.session_state.hours_per_day,
                            "target_months": st.session_state.target_months,
                        }
                    resp = api_client.chat(
                        sug, st.session_state.chat_history[:-1], profile_data
                    )
                    if resp:
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": resp["reply"]}
                        )
                        st.session_state["_last_suggestions"] = resp.get(
                            "suggestions", []
                        )
                    st.rerun()

# ─── Chat Input ──────────────────────────────────────────────────
if prompt := st.chat_input("Ask me anything about your career journey..."):
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👩"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant", avatar="💜"):
        with st.spinner("Thinking..."):
            profile_data = None
            if st.session_state.form_submitted:
                profile_data = {
                    "name": st.session_state.user_name,
                    "education": st.session_state.education,
                    "previous_job": st.session_state.previous_job,
                    "career_gap_years": st.session_state.career_gap_years,
                    "skills": st.session_state.skills,
                    "interests": st.session_state.interests,
                    "goal_role": st.session_state.goal_role,
                    "hours_per_day": st.session_state.hours_per_day,
                    "target_months": st.session_state.target_months,
                }
            response = api_client.chat(
                prompt, st.session_state.chat_history[:-1], profile_data
            )

            if response:
                reply = response["reply"]
                st.markdown(reply)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": reply}
                )
                st.session_state["_last_suggestions"] = response.get(
                    "suggestions", []
                )
            else:
                error_msg = "I'm having trouble connecting right now. Please make sure the backend server is running."
                st.markdown(error_msg)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": error_msg}
                )

    # Rerun to show suggestions
    if response and response.get("suggestions"):
        st.rerun()

# ─── Empty State ─────────────────────────────────────────────────
if not st.session_state.chat_history:
    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <h3>👋 Welcome to your AI Career Coach!</h3>
            <p>I'm here to help you navigate your career comeback. You can ask me about:<br><br>
            📄 Resume writing & career gap explanations<br>
            🎤 Interview preparation & common questions<br>
            💰 Salary negotiation strategies<br>
            🤝 Networking tips & community recommendations<br>
            🎓 Certifications & upskilling paths<br>
            💪 Building confidence for your return<br><br>
            <em>Tap a quick topic above or type your question below!</em></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.form_submitted:
        st.info(
            "💡 **Tip:** Fill out your profile on the 🏠 Home page first for personalized advice!"
        )

"""
🏠 Home — Career Intake Form

This is the main entry point for the Women's Career Counselor.
Collects user profile information and stores it in session state.
"""

import streamlit as st
from utils.state import init_session_state
from utils.styles import inject_custom_css

# ─── Page Configuration ──────────────────────────────────────────
st.set_page_config(
    page_title="CareerHer — AI Career Counselor for Women",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Initialize ──────────────────────────────────────────────────
init_session_state()
st.markdown(inject_custom_css(), unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💜 CareerHer")
    st.markdown("*AI-Powered Career Counselor*")
    st.divider()
    st.markdown(
        """
        **How it works:**
        1. 📝 Fill out your profile
        2. 📊 Get AI-powered insights
        3. 💬 Chat with your career coach
        """
    )
    st.divider()
    st.caption("Powered by Google Gemini AI")

# ─── Hero Section ────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-container">
        <h1>💜 CareerHer</h1>
        <p>Your AI-powered career counselor — designed for women restarting their careers.<br>
        Tell us about yourself, and we'll create your personalized career roadmap.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Skills and Interests Catalogs ───────────────────────────────
SKILLS_OPTIONS = [
    "Python", "JavaScript", "SQL", "Excel", "Data Analysis",
    "Machine Learning", "Web Development", "Cloud Computing",
    "Cybersecurity", "UI/UX Design", "Project Management",
    "Strategic Planning", "Business Analysis", "Financial Planning",
    "Operations Management", "Team Leadership", "Budgeting",
    "Process Improvement", "Technical Writing", "Content Creation",
    "Public Speaking", "Social Media Marketing", "Graphic Design",
    "Video Editing", "Copywriting", "Customer Service",
    "Negotiation", "Conflict Resolution", "Mentoring",
    "Cross-cultural Communication", "Healthcare Administration",
    "Legal Research", "Accounting", "Human Resources",
    "Supply Chain Management", "Teaching/Training",
    "Research & Development", "Quality Assurance",
    "Event Planning", "Fundraising/Grants",
]

INTERESTS_OPTIONS = [
    "Technology", "Healthcare", "Education", "Finance",
    "Marketing & Advertising", "Non-Profit / Social Impact",
    "Media & Entertainment", "E-Commerce / Retail", "Consulting",
    "Government & Public Policy", "Real Estate",
    "Sustainability & Environment", "Arts & Design", "Legal",
    "Human Resources", "Science & Research",
]

EDUCATION_OPTIONS = [
    "High School", "Associate's", "Bachelor's", "Master's",
    "PhD", "Bootcamp/Certification",
]

# ─── Intake Form ─────────────────────────────────────────────────
st.markdown(
    '<div class="section-header"><h2>📝 Your Profile</h2></div>',
    unsafe_allow_html=True,
)

with st.form("intake_form", clear_on_submit=False):
    # Row 1: Name and Education
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(
            "👤 Your Name",
            value=st.session_state.user_name,
            placeholder="e.g., Priya Sharma",
            key="form_name",
        )
    with col2:
        education = st.selectbox(
            "🎓 Highest Education",
            options=EDUCATION_OPTIONS,
            index=EDUCATION_OPTIONS.index(st.session_state.education)
            if st.session_state.education in EDUCATION_OPTIONS
            else 2,
            key="form_education",
        )

    # Row 2: Previous Job and Goal Role
    col3, col4 = st.columns(2)
    with col3:
        previous_job = st.text_input(
            "💼 Previous/Most Recent Job Title",
            value=st.session_state.previous_job,
            placeholder="e.g., Marketing Manager",
            key="form_previous_job",
        )
    with col4:
        goal_role = st.text_input(
            "🎯 Target Role / Career Direction",
            value=st.session_state.goal_role,
            placeholder="e.g., Data Analyst, UX Designer",
            key="form_goal_role",
        )

    # Row 3: Sliders
    col5, col6, col7 = st.columns(3)
    with col5:
        career_gap = st.slider(
            "⏸️ Career Gap (years)",
            min_value=0.0,
            max_value=15.0,
            value=float(st.session_state.career_gap_years),
            step=0.5,
            key="form_career_gap",
        )
    with col6:
        hours = st.slider(
            "⏰ Hours Available per Day",
            min_value=1,
            max_value=12,
            value=st.session_state.hours_per_day,
            key="form_hours",
        )
    with col7:
        months = st.slider(
            "📅 Target Timeline (months)",
            min_value=1,
            max_value=24,
            value=st.session_state.target_months,
            key="form_months",
        )

    # Row 4: Multiselects
    skills = st.multiselect(
        "🛠️ Your Current Skills (select all that apply)",
        options=SKILLS_OPTIONS,
        default=st.session_state.skills
        if st.session_state.skills
        else None,
        key="form_skills",
        help="Choose skills you already possess — we'll identify gaps for your target role",
    )

    interests = st.multiselect(
        "🌟 Industries / Fields of Interest",
        options=INTERESTS_OPTIONS,
        default=st.session_state.interests
        if st.session_state.interests
        else None,
        key="form_interests",
        help="Pick industries that excite you — this helps us match careers",
    )

    st.markdown("---")

    # Submit
    submitted = st.form_submit_button(
        "🚀 Analyze My Career Options",
        use_container_width=True,
    )

    if submitted:
        # Validate required fields
        errors = []
        if not name.strip():
            errors.append("Please enter your name")
        if not previous_job.strip():
            errors.append("Please enter your previous job title")
        if not goal_role.strip():
            errors.append("Please enter your target role")
        if not skills:
            errors.append("Please select at least one skill")
        if not interests:
            errors.append("Please select at least one interest")

        if errors:
            for error in errors:
                st.error(f"⚠️ {error}")
        else:
            # Save to session state
            st.session_state.user_name = name.strip()
            st.session_state.education = education
            st.session_state.previous_job = previous_job.strip()
            st.session_state.career_gap_years = career_gap
            st.session_state.skills = skills
            st.session_state.interests = interests
            st.session_state.goal_role = goal_role.strip()
            st.session_state.hours_per_day = hours
            st.session_state.target_months = months
            st.session_state.form_submitted = True

            # Clear previous results
            st.session_state.analysis_result = None
            st.session_state.score_result = None
            st.session_state.roadmap_result = None
            st.session_state.selected_career = None

            st.success("✅ Profile saved! Navigate to the **📊 Results** page to see your analysis.")
            st.balloons()

# ─── Profile Summary (if submitted) ─────────────────────────────
if st.session_state.form_submitted:
    st.markdown("---")
    st.markdown(
        '<div class="section-header"><h2>✅ Profile Summary</h2></div>',
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown(
            f"""
            <div class="glass-card">
                <h3>👤 {st.session_state.user_name}</h3>
                <p>🎓 {st.session_state.education}<br>
                💼 Previously: {st.session_state.previous_job}<br>
                ⏸️ {st.session_state.career_gap_years} year gap</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        skills_str = ", ".join(st.session_state.skills[:5])
        if len(st.session_state.skills) > 5:
            skills_str += f" +{len(st.session_state.skills) - 5} more"
        st.markdown(
            f"""
            <div class="glass-card">
                <h3>🛠️ Skills & Interests</h3>
                <p>Skills: {skills_str}<br>
                Interests: {', '.join(st.session_state.interests[:3])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_c:
        st.markdown(
            f"""
            <div class="glass-card">
                <h3>🎯 Goals</h3>
                <p>Target: {st.session_state.goal_role}<br>
                ⏰ {st.session_state.hours_per_day} hrs/day<br>
                📅 {st.session_state.target_months} month timeline</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info("👉 Head to the **📊 Results** page in the sidebar to see your AI-powered analysis!")

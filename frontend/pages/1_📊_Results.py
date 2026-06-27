"""
📊 Results Dashboard

Displays AI-powered career analysis results including:
- Employability score (gauge chart)
- 3 career cards
- Skill gap table (have/need columns)
- 30/60/90 day roadmap in tabs
"""

import streamlit as st
import plotly.graph_objects as go

from utils.state import init_session_state
from utils.styles import inject_custom_css
from utils import api_client

# ─── Page Configuration ──────────────────────────────────────────
st.set_page_config(
    page_title="Results — CareerHer",
    page_icon="📊",
    layout="wide",
)

# ─── Initialize ──────────────────────────────────────────────────
init_session_state()
st.markdown(inject_custom_css(), unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💜 CareerHer")
    st.markdown("*Results Dashboard*")
    st.divider()
    if st.session_state.form_submitted:
        st.success(f"👤 {st.session_state.user_name}")
        st.caption(f"🎯 Target: {st.session_state.goal_role}")
    if st.button("🔄 Re-analyze", use_container_width=True):
        st.session_state.analysis_result = None
        st.session_state.score_result = None
        st.session_state.roadmap_result = None
        st.rerun()

# ─── Check if form submitted ────────────────────────────────────
if not st.session_state.form_submitted:
    st.markdown(
        """
        <div class="hero-container">
            <h1>📊 Results Dashboard</h1>
            <p>Complete the intake form on the Home page first to see your personalized career analysis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.warning("👈 Please fill out your profile on the **🏠 Home** page first.")
    st.stop()

# ─── Hero ────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="hero-container">
        <h1>📊 Your Career Analysis</h1>
        <p>Personalized insights for {st.session_state.user_name} — powered by AI</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Fetch Data ──────────────────────────────────────────────────
# Fetch analysis and score if not already loaded
if st.session_state.analysis_result is None:
    with st.spinner("🤖 AI is analyzing your profile..."):
        st.session_state.analysis_result = api_client.analyze_profile()

if st.session_state.score_result is None:
    with st.spinner("📊 Calculating your employability score..."):
        st.session_state.score_result = api_client.get_score()

analysis = st.session_state.analysis_result
score_data = st.session_state.score_result

if not analysis or not score_data:
    st.error("Failed to load analysis. Please check that the backend server is running.")
    st.stop()


# ═══════════════════════════════════════════════════════════════════
# SECTION 1: EMPLOYABILITY SCORE
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header"><h2>🏆 Employability Score</h2></div>',
    unsafe_allow_html=True,
)

score_col, breakdown_col = st.columns([1, 1])

with score_col:
    overall = score_data["overall_score"]

    # Determine color based on score
    if overall >= 80:
        bar_color = "#22C55E"
    elif overall >= 60:
        bar_color = "#06B6D4"
    elif overall >= 40:
        bar_color = "#F59E0B"
    else:
        bar_color = "#F472B6"

    # Plotly gauge chart
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=overall,
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "font": {"size": 60, "color": "#F1F5F9", "family": "Inter"},
                "suffix": "/100",
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#475569",
                    "dtick": 20,
                    "tickfont": {"color": "#94A3B8"},
                },
                "bar": {"color": bar_color, "thickness": 0.8},
                "bgcolor": "#1E293B",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "rgba(244, 114, 182, 0.1)"},
                    {"range": [40, 60], "color": "rgba(245, 158, 11, 0.1)"},
                    {"range": [60, 80], "color": "rgba(6, 182, 212, 0.1)"},
                    {"range": [80, 100], "color": "rgba(34, 197, 94, 0.1)"},
                ],
                "threshold": {
                    "line": {"color": "#F1F5F9", "width": 3},
                    "thickness": 0.8,
                    "value": overall,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#F1F5F9", "family": "Inter"},
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Verdict badge
    verdict = score_data.get("verdict", "Almost There")
    verdict_class = {
        "Ready": "verdict-ready",
        "Almost There": "verdict-almost",
        "Needs Work": "verdict-needs",
        "Getting Started": "verdict-starting",
    }.get(verdict, "verdict-almost")

    st.markdown(
        f'<div style="text-align:center"><span class="verdict-badge {verdict_class}">{verdict}</span></div>',
        unsafe_allow_html=True,
    )

with breakdown_col:
    st.markdown("#### Score Breakdown")
    breakdown = score_data.get("breakdown", {})

    metrics = [
        ("🎓 Education", breakdown.get("education_score", 0)),
        ("🛠️ Skills", breakdown.get("skills_score", 0)),
        ("💼 Experience Relevance", breakdown.get("experience_relevance", 0)),
        ("📈 Market Demand", breakdown.get("market_demand", 0)),
        ("⏸️ Gap Impact", breakdown.get("gap_impact", 0)),
    ]

    for label, value in metrics:
        col_label, col_bar = st.columns([1, 2])
        with col_label:
            st.markdown(f"**{label}**")
        with col_bar:
            st.progress(value / 100, text=f"{value}/100")

    st.markdown("---")
    st.markdown("#### 💡 Top Recommendations")
    for rec in score_data.get("recommendations", [])[:4]:
        st.markdown(f"• {rec}")


# ═══════════════════════════════════════════════════════════════════
# SECTION 2: CAREER CARDS
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header"><h2>🎯 Career Recommendations</h2></div>',
    unsafe_allow_html=True,
)

careers = analysis.get("career_cards", [])
summary = analysis.get("summary", "")

if summary:
    st.markdown(
        f"""
        <div class="glass-card">
            <p>{summary}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

cols = st.columns(len(careers)) if careers else []

for idx, (col, career) in enumerate(zip(cols, careers)):
    with col:
        skills_tags = "".join(
            f'<span class="skill-tag">{s}</span>' for s in career.get("required_skills", [])
        )
        st.markdown(
            f"""
            <div class="career-card">
                <span class="match-badge">🎯 {career.get('match_percentage', 0)}% Match</span>
                <div class="career-title">{career.get('title', 'Career')}</div>
                <div class="career-desc">{career.get('description', '')}</div>
                <div>{skills_tags}</div>
                <div style="margin-top: 0.8rem">
                    <span class="growth-badge">📈 {career.get('growth_outlook', 'Stable')}</span>
                    <span class="salary-badge">💰 {career.get('avg_salary', 'Varies')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Career selection for roadmap
if careers:
    st.markdown("---")
    career_titles = [c.get("title", f"Career {i+1}") for i, c in enumerate(careers)]

    def on_career_change():
        st.session_state.roadmap_result = None

    selected = st.selectbox(
        "🗺️ Select a career path to generate your personalized roadmap:",
        options=career_titles,
        index=0,
        key="career_selector",
        on_change=on_career_change,
    )
    st.session_state.selected_career = selected


# ═══════════════════════════════════════════════════════════════════
# SECTION 3: SKILL GAP TABLE
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header"><h2>🛠️ Skill Gap Analysis</h2></div>',
    unsafe_allow_html=True,
)

skill_gaps = analysis.get("skill_gaps", [])
have_skills = [s for s in skill_gaps if s.get("category") == "have"]
need_skills = [s for s in skill_gaps if s.get("category") == "need"]

col_have, col_need = st.columns(2)

with col_have:
    st.markdown("#### ✅ Skills You Have")
    if have_skills:
        for skill in have_skills:
            level = skill.get("proficiency_level", "Intermediate")
            st.markdown(
                f"""
                <div class="skill-have">
                    {skill.get('skill_name', '')}
                    <span class="skill-level">{level}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Your skills will appear here after analysis.")

with col_need:
    st.markdown("#### 📚 Skills You Need")
    if need_skills:
        for skill in need_skills:
            level = skill.get("proficiency_level", "Beginner")
            priority = skill.get("priority", "Medium")
            priority_class = f"priority-{priority.lower()}"
            st.markdown(
                f"""
                <div class="skill-need">
                    {skill.get('skill_name', '')}
                    <span class="skill-level">
                        {level} · <span class="{priority_class}">{priority} Priority</span>
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Required skills will appear here after analysis.")


# ═══════════════════════════════════════════════════════════════════
# SECTION 4: 30/60/90 DAY ROADMAP
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header"><h2>🗺️ 30 / 60 / 90 Day Roadmap</h2></div>',
    unsafe_allow_html=True,
)

# Fetch roadmap for selected career
selected_career = st.session_state.get("selected_career")
if selected_career:
    if st.session_state.roadmap_result is None:
        with st.spinner(f"🗺️ Generating roadmap for {selected_career}..."):
            st.session_state.roadmap_result = api_client.get_roadmap(selected_career)

    roadmap = st.session_state.roadmap_result

    if roadmap:
        if roadmap.get("summary"):
            st.markdown(
                f"""
                <div class="glass-card">
                    <p>{roadmap['summary']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        tab1, tab2, tab3 = st.tabs([
            "🌱 Days 1-30: Foundation",
            "🔨 Days 31-60: Building",
            "🚀 Days 61-90: Launch",
        ])

        def render_tasks(tasks):
            """Render a list of roadmap tasks."""
            for i, task in enumerate(tasks, 1):
                st.markdown(
                    f"""
                    <div class="roadmap-task">
                        <div class="task-title">📌 {i}. {task.get('task', '')}</div>
                        <div class="task-resource">📖 {task.get('resource', '')}</div>
                        <div class="task-milestone">🏁 {task.get('milestone', '')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with tab1:
            render_tasks(roadmap.get("day_30", []))

        with tab2:
            render_tasks(roadmap.get("day_60", []))

        with tab3:
            render_tasks(roadmap.get("day_90", []))
    else:
        st.warning("Could not generate roadmap. Please check the backend connection.")
else:
    st.info("👆 Select a career path above to generate your personalized roadmap.")

# ─── Footer ──────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 1rem 0;">
        💜 CareerHer — AI-powered career guidance for women returning to work<br>
        <em>Your career break is not a setback — it's a unique perspective.</em>
    </div>
    """,
    unsafe_allow_html=True,
)

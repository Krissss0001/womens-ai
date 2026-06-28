"""Google Gemini AI service — embedded directly in the Streamlit frontend.

This module replaces the FastAPI backend calls so the app works
on Streamlit Cloud without a separate server.
"""

import json
import logging
import os
import re
from typing import Any

logger = logging.getLogger(__name__)

# ── Prompt templates ──────────────────────────────────────────────

ANALYZE_PROMPT = """You are an expert career counselor specializing in helping women restart their careers after a career break.

Analyze the following profile and provide career recommendations.

**User Profile:**
- Name: {name}
- Education: {education}
- Previous Job: {previous_job}
- Career Gap: {career_gap_years} years
- Current Skills: {skills}
- Interests: {interests}
- Goal Role: {goal_role}
- Available Hours/Day: {hours_per_day}
- Target Timeline: {target_months} months

Provide your analysis as a JSON object with this exact structure:
{{
    "career_cards": [
        {{
            "title": "Career Title",
            "match_percentage": 85,
            "description": "Brief description of why this is a good fit",
            "required_skills": ["skill1", "skill2", "skill3"],
            "growth_outlook": "High Growth",
            "avg_salary": "$60,000 - $80,000"
        }}
    ],
    "skill_gaps": [
        {{
            "skill_name": "Skill Name",
            "category": "have",
            "proficiency_level": "Intermediate",
            "priority": "High"
        }}
    ],
    "summary": "Overall analysis summary paragraph",
    "strengths": ["strength1", "strength2", "strength3"]
}}

Rules:
- Provide exactly 3 career cards, ranked by match percentage
- Include ALL user's existing skills in skill_gaps with category "have"
- Include 5-8 skills they need with category "need"
- Be encouraging and supportive in tone
- Consider the career gap duration and suggest realistic transitions
- Focus on careers with strong remote/flexible work options when possible
- Return ONLY the JSON object, no other text
"""

SCORE_PROMPT = """You are an employability assessment expert specializing in career re-entry for women.

Evaluate the employability of the following candidate and provide a detailed score.

**User Profile:**
- Name: {name}
- Education: {education}
- Previous Job: {previous_job}
- Career Gap: {career_gap_years} years
- Current Skills: {skills}
- Interests: {interests}
- Goal Role: {goal_role}
- Available Hours/Day: {hours_per_day}
- Target Timeline: {target_months} months

Provide your assessment as a JSON object with this exact structure:
{{
    "overall_score": 72,
    "breakdown": {{
        "education_score": 80,
        "skills_score": 65,
        "experience_relevance": 70,
        "market_demand": 75,
        "gap_impact": 60
    }},
    "recommendations": [
        "Specific actionable recommendation 1",
        "Specific actionable recommendation 2",
        "Specific actionable recommendation 3"
    ],
    "verdict": "Almost There"
}}

Rules:
- All scores must be between 0 and 100
- overall_score should be a weighted average (education 20%, skills 25%, experience 20%, market_demand 20%, gap_impact 15%)
- gap_impact: higher score = less negative impact (shorter gap or transferable skills)
- verdict must be one of: "Ready", "Almost There", "Needs Work", "Getting Started"
- Provide 4-6 specific, actionable recommendations
- Be realistic but encouraging
- Return ONLY the JSON object, no other text
"""

ROADMAP_PROMPT = """You are a career development strategist creating a 30/60/90 day action plan for women re-entering the workforce.

Create a detailed roadmap for the following candidate targeting a specific career.

**User Profile:**
- Name: {name}
- Education: {education}
- Previous Job: {previous_job}
- Career Gap: {career_gap_years} years
- Current Skills: {skills}
- Interests: {interests}
- Goal Role: {goal_role}
- Available Hours/Day: {hours_per_day}
- Target Timeline: {target_months} months

**Selected Career Path:** {selected_career}

Provide the roadmap as a JSON object with this exact structure:
{{
    "day_30": [
        {{
            "task": "Specific task description",
            "resource": "Platform, course, or tool name with URL if applicable",
            "milestone": "Measurable outcome"
        }}
    ],
    "day_60": [
        {{
            "task": "Specific task description",
            "resource": "Platform, course, or tool name",
            "milestone": "Measurable outcome"
        }}
    ],
    "day_90": [
        {{
            "task": "Specific task description",
            "resource": "Platform, course, or tool name",
            "milestone": "Measurable outcome"
        }}
    ],
    "summary": "Brief overview of the 90-day journey"
}}

Rules:
- Day 30 (Foundation): 4-5 tasks focused on learning fundamentals and updating professional presence
- Day 60 (Building): 4-5 tasks focused on skill development and portfolio building
- Day 90 (Launch): 4-5 tasks focused on job applications, networking, and interview prep
- Include specific free/affordable resources (Coursera, LinkedIn Learning, YouTube, etc.)
- Milestones must be measurable and concrete
- Account for their available hours per day
- Include at least one networking/community task per phase
- Return ONLY the JSON object, no other text
"""

CHAT_SYSTEM_PROMPT = """You are CareerCounselor AI, a warm, knowledgeable, and empowering career counselor \
who specializes in helping women restart their careers after a career break.

Your personality traits:
- Encouraging and supportive, never judgmental about career gaps
- Practical and action-oriented — give specific, actionable advice
- Knowledgeable about current job market trends, remote work, and flexible careers
- Aware of challenges women face re-entering the workforce (confidence gap, skills gap, ageism, etc.)
- You celebrate small wins and help build confidence

If the user has a profile, here it is:
{profile_context}

Guidelines:
- Keep responses conversational but informative (2-4 paragraphs max)
- Always end with an encouraging note or actionable next step
- Suggest specific resources when relevant (courses, platforms, communities)
- If asked about salary, provide realistic ranges based on location and experience
- Be honest about challenges but frame them as surmountable
- Use inclusive, empowering language

At the end of each response, suggest 2-3 follow-up questions the user might want to ask, \
formatted as a JSON array on the last line like:
SUGGESTIONS: ["Question 1?", "Question 2?", "Question 3?"]
"""

# ── Helper functions ───────────────────────────────────────────────

def _get_api_key() -> str:
    """Get Google API key from Streamlit secrets or environment."""
    try:
        import streamlit as st
        key = st.secrets.get("GOOGLE_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return os.environ.get("GOOGLE_API_KEY", "")


def _is_configured() -> bool:
    key = _get_api_key()
    return bool(key and key != "your_google_api_key_here" and len(key) > 10)


def _get_model_name() -> str:
    try:
        import streamlit as st
        return st.secrets.get("GEMINI_MODEL", "gemini-1.5-flash")
    except Exception:
        return os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")


def _extract_json(text: str) -> dict[str, Any]:
    """Extract JSON from Gemini response, handling markdown code blocks."""
    cleaned = re.sub(r"```(?:json)?\s*", "", text)
    cleaned = re.sub(r"```", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not extract valid JSON from response: {text[:200]}...")


def _call_gemini(prompt: str) -> str:
    """Call Gemini API and return raw text."""
    from google import genai
    client = genai.Client(api_key=_get_api_key())
    response = client.models.generate_content(
        model=_get_model_name(),
        contents=prompt,
    )
    return response.text


def _format_profile(profile: dict) -> dict:
    return {
        "name": profile.get("name", "User"),
        "education": profile.get("education", "Bachelor's"),
        "previous_job": profile.get("previous_job", "Professional"),
        "career_gap_years": str(profile.get("career_gap_years", 2)),
        "skills": ", ".join(profile.get("skills", [])),
        "interests": ", ".join(profile.get("interests", [])),
        "goal_role": profile.get("goal_role", "Professional"),
        "hours_per_day": str(profile.get("hours_per_day", 4)),
        "target_months": str(profile.get("target_months", 6)),
    }

# ── Public API ────────────────────────────────────────────────────

def analyze_profile(profile: dict) -> dict[str, Any]:
    """Analyze user profile and return career recommendations."""
    if not _is_configured():
        return _mock_analysis(profile)
    try:
        prompt = ANALYZE_PROMPT.format(**_format_profile(profile))
        return _extract_json(_call_gemini(prompt))
    except Exception as e:
        logger.error(f"Gemini analyze error: {e}")
        return _mock_analysis(profile)


def calculate_score(profile: dict) -> dict[str, Any]:
    """Calculate employability score."""
    if not _is_configured():
        return _mock_score(profile)
    try:
        prompt = SCORE_PROMPT.format(**_format_profile(profile))
        return _extract_json(_call_gemini(prompt))
    except Exception as e:
        logger.error(f"Gemini score error: {e}")
        return _mock_score(profile)


def generate_roadmap(profile: dict, selected_career: str) -> dict[str, Any]:
    """Generate 30/60/90 day roadmap."""
    if not _is_configured():
        return _mock_roadmap(profile, selected_career)
    try:
        fmt = _format_profile(profile)
        fmt["selected_career"] = selected_career
        prompt = ROADMAP_PROMPT.format(**fmt)
        return _extract_json(_call_gemini(prompt))
    except Exception as e:
        logger.error(f"Gemini roadmap error: {e}")
        return _mock_roadmap(profile, selected_career)


def chat(message: str, history: list[dict], profile: dict | None = None) -> dict[str, Any]:
    """Career coaching chat."""
    if not _is_configured():
        return _mock_chat(message)
    try:
        if profile:
            profile_ctx = (
                f"Name: {profile.get('name')}, Education: {profile.get('education')}, "
                f"Previous Job: {profile.get('previous_job')}, "
                f"Career Gap: {profile.get('career_gap_years')} years, "
                f"Skills: {', '.join(profile.get('skills', []))}, "
                f"Goal: {profile.get('goal_role')}"
            )
        else:
            profile_ctx = "No profile provided yet."

        system_prompt = CHAT_SYSTEM_PROMPT.format(profile_context=profile_ctx)
        contents = [system_prompt]
        for msg in history:
            contents.append(f"{msg['role']}: {msg['content']}")
        contents.append(f"user: {message}")
        full_prompt = "\n\n".join(contents)

        text = _call_gemini(full_prompt)

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
        return _mock_chat(message)

# ── Mock / fallback responses ─────────────────────────────────────

def _mock_analysis(profile: dict) -> dict[str, Any]:
    name = profile.get("name", "there")
    prev = profile.get("previous_job", "your previous role")
    edu = profile.get("education", "your education")
    gap = profile.get("career_gap_years", 2)
    skills = profile.get("skills", [])
    hours = profile.get("hours_per_day", 4)
    return {
        "career_cards": [
            {
                "title": "Project Manager",
                "match_percentage": 88,
                "description": (
                    f"Your background in {prev} provides strong foundational skills for "
                    f"project management. With your {edu} education and organizational skills, "
                    "this is an excellent transition path."
                ),
                "required_skills": ["Agile/Scrum", "Stakeholder Management", "Risk Assessment", "Budgeting", "Communication"],
                "growth_outlook": "High Growth",
                "avg_salary": "$65,000 - $95,000",
            },
            {
                "title": "UX Researcher",
                "match_percentage": 76,
                "description": "Your interpersonal skills and analytical thinking make UX research a great fit. This field values diverse perspectives and career changers.",
                "required_skills": ["User Interviews", "Data Analysis", "Wireframing", "A/B Testing", "Empathy Mapping"],
                "growth_outlook": "High Growth",
                "avg_salary": "$70,000 - $110,000",
            },
            {
                "title": "Digital Marketing Specialist",
                "match_percentage": 72,
                "description": "Digital marketing offers flexible work arrangements and values creativity alongside analytical skills. Many certifications are available online.",
                "required_skills": ["SEO/SEM", "Content Strategy", "Google Analytics", "Social Media", "Email Marketing"],
                "growth_outlook": "Stable Growth",
                "avg_salary": "$50,000 - $80,000",
            },
        ],
        "skill_gaps": [
            *[{"skill_name": s, "category": "have", "proficiency_level": "Intermediate", "priority": "Medium"} for s in skills[:6]],
            {"skill_name": "Agile Methodology", "category": "need", "proficiency_level": "Beginner", "priority": "High"},
            {"skill_name": "Data Analytics", "category": "need", "proficiency_level": "Beginner", "priority": "High"},
            {"skill_name": "Digital Tools Proficiency", "category": "need", "proficiency_level": "Beginner", "priority": "Medium"},
            {"skill_name": "Industry Networking", "category": "need", "proficiency_level": "Beginner", "priority": "High"},
            {"skill_name": "Portfolio Building", "category": "need", "proficiency_level": "Beginner", "priority": "Medium"},
        ],
        "summary": (
            f"Great news, {name}! Based on your profile, you have a solid foundation for re-entering the workforce. "
            f"Your experience as a {prev} and your {edu} education give you transferable skills that are highly valued. "
            f"While a {gap}-year gap may feel daunting, many employers now actively seek career returners."
        ),
        "strengths": [
            "Strong educational foundation",
            "Transferable professional experience",
            "Clear career direction",
            f"Commitment to {hours} hours/day of development",
        ],
    }


def _mock_score(profile: dict) -> dict[str, Any]:
    gap = profile.get("career_gap_years", 2)
    skills = profile.get("skills", [])
    edu = profile.get("education", "Bachelor's")
    hours = profile.get("hours_per_day", 4)
    goal = profile.get("goal_role", "your target role")

    gap_penalty = max(0, 100 - int(gap * 8))
    skills_score = min(100, len(skills) * 12)
    edu_map = {"High School": 50, "Associate's": 60, "Bachelor's": 75, "Master's": 85, "PhD": 90, "Bootcamp/Certification": 70}
    edu_score = edu_map.get(edu, 65)
    overall = int(edu_score * 0.20 + skills_score * 0.25 + 65 * 0.20 + 70 * 0.20 + gap_penalty * 0.15)

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
            f"Complete a certification in {goal}-related skills",
            "Update your LinkedIn profile with a career narrative that frames your gap positively",
            "Join 2-3 professional communities in your target industry",
            "Build a portfolio with 2-3 projects showcasing your skills",
            f"Dedicate your {hours} daily hours to structured learning",
        ],
        "verdict": verdict,
    }


def _mock_roadmap(profile: dict, selected_career: str) -> dict[str, Any]:
    name = profile.get("name", "you")
    hours = profile.get("hours_per_day", 4)
    return {
        "day_30": [
            {"task": f"Complete an introductory course on {selected_career} fundamentals", "resource": "Coursera / LinkedIn Learning (free audit)", "milestone": "Earn course completion certificate"},
            {"task": "Update LinkedIn profile with career-returner narrative", "resource": "LinkedIn.com — use career break feature", "milestone": "Profile completeness score above 90%"},
            {"task": "Join 3 professional communities and women-in-tech groups", "resource": "LinkedIn Groups, Women Who Code, Elpha", "milestone": "Active member in 3 communities"},
            {"task": "Set up a professional portfolio website", "resource": "GitHub Pages, Notion, or WordPress", "milestone": "Live portfolio URL with bio and skills"},
        ],
        "day_60": [
            {"task": f"Complete an intermediate {selected_career} skills course", "resource": "Udemy, Google Career Certificates", "milestone": "Intermediate certification earned"},
            {"task": "Build 2 portfolio projects demonstrating key skills", "resource": "GitHub, personal projects", "milestone": "2 completed projects in portfolio"},
            {"task": "Attend 2 virtual networking events or webinars", "resource": "Eventbrite, Meetup.com", "milestone": "Made 5+ new professional connections"},
            {"task": "Start informational interviews with people in target role", "resource": "LinkedIn outreach", "milestone": "Completed 3 informational interviews"},
        ],
        "day_90": [
            {"task": "Craft a tailored resume for target role", "resource": "Resume templates from Indeed, TopResume", "milestone": "ATS-optimized resume ready"},
            {"task": "Practice mock interviews with common questions", "resource": "Pramp.com, Interview Warmup by Google", "milestone": "Completed 5 mock interviews"},
            {"task": "Apply to 15-20 positions matching your profile", "resource": "LinkedIn Jobs, Indeed, Glassdoor", "milestone": "Submitted 15+ tailored applications"},
            {"task": "Reach out to recruiters specializing in career returners", "resource": "Path Forward, iRelaunch, LinkedIn Recruiters", "milestone": "Connected with 3+ recruiters"},
        ],
        "summary": (
            f"This 90-day plan is designed to help {name} transition into {selected_career} "
            f"with {hours} hours/day of dedicated effort. Phase 1 builds your foundation, "
            "Phase 2 develops your skills and network, and Phase 3 launches your job search."
        ),
    }


def _mock_chat(message: str) -> dict[str, Any]:
    return {
        "reply": (
            "Thank you for your question! I'm running in demo mode right now "
            "(no API key configured), but I want you to know that you're already "
            "taking a fantastic step by exploring your career options.\n\n"
            "When fully configured with a Google API key, I can provide fully personalised advice. "
            "Add your **GOOGLE_API_KEY** in the Streamlit Cloud secrets to enable AI features."
        ),
        "suggestions": [
            "How do I explain my career gap in interviews?",
            "What are the best certifications for career changers?",
            "How can I build a professional network from scratch?",
        ],
    }

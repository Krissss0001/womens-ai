"""Business logic helpers for career analysis.

Provides utility functions used across endpoints for
data transformation and validation.
"""

from app.schemas.requests import UserProfile


# Curated skills list for the frontend multiselect
SKILLS_CATALOG = [
    # Technical
    "Python",
    "JavaScript",
    "SQL",
    "Excel",
    "Data Analysis",
    "Machine Learning",
    "Web Development",
    "Cloud Computing",
    "Cybersecurity",
    "UI/UX Design",
    # Business & Management
    "Project Management",
    "Strategic Planning",
    "Business Analysis",
    "Financial Planning",
    "Operations Management",
    "Team Leadership",
    "Budgeting",
    "Process Improvement",
    # Communication & Creative
    "Technical Writing",
    "Content Creation",
    "Public Speaking",
    "Social Media Marketing",
    "Graphic Design",
    "Video Editing",
    "Copywriting",
    # Interpersonal
    "Customer Service",
    "Negotiation",
    "Conflict Resolution",
    "Mentoring",
    "Cross-cultural Communication",
    # Domain Specific
    "Healthcare Administration",
    "Legal Research",
    "Accounting",
    "Human Resources",
    "Supply Chain Management",
    "Teaching/Training",
    "Research & Development",
    "Quality Assurance",
    "Event Planning",
    "Fundraising/Grants",
]

INTERESTS_CATALOG = [
    "Technology",
    "Healthcare",
    "Education",
    "Finance",
    "Marketing & Advertising",
    "Non-Profit / Social Impact",
    "Media & Entertainment",
    "E-Commerce / Retail",
    "Consulting",
    "Government & Public Policy",
    "Real Estate",
    "Sustainability & Environment",
    "Arts & Design",
    "Legal",
    "Human Resources",
    "Science & Research",
]

EDUCATION_LEVELS = [
    "High School",
    "Associate's",
    "Bachelor's",
    "Master's",
    "PhD",
    "Bootcamp/Certification",
]


def validate_profile_completeness(profile: UserProfile) -> list[str]:
    """Check profile completeness, return list of warnings."""
    warnings = []
    if len(profile.skills) < 2:
        warnings.append("Consider adding more skills for a better analysis.")
    if len(profile.interests) < 1:
        warnings.append("Adding interests helps us match you with the right careers.")
    if profile.hours_per_day < 2:
        warnings.append(
            "With limited daily hours, progress may be slower — that's okay!"
        )
    return warnings

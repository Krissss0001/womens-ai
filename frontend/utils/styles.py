"""Custom CSS styles for the Streamlit frontend.

Injects modern glassmorphism, gradient animations, and premium
typography into the Streamlit app via st.markdown().
"""


def inject_custom_css():
    """Return the custom CSS string to inject via st.markdown."""
    return """
<style>
    /* ─── Google Fonts ─────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ─── Root Variables ───────────────────────────────────────── */
    :root {
        --primary: #7C3AED;
        --primary-light: #A78BFA;
        --secondary: #06B6D4;
        --accent: #F472B6;
        --bg-dark: #0F172A;
        --bg-surface: #1E293B;
        --bg-glass: rgba(30, 41, 59, 0.7);
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --border-subtle: rgba(148, 163, 184, 0.15);
        --gradient-primary: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%);
        --gradient-accent: linear-gradient(135deg, #F472B6 0%, #7C3AED 100%);
        --gradient-warm: linear-gradient(135deg, #F59E0B 0%, #F472B6 100%);
        --shadow-glow: 0 0 40px rgba(124, 58, 237, 0.15);
        --radius-lg: 16px;
        --radius-md: 12px;
        --radius-sm: 8px;
    }

    /* ─── Global Overrides ─────────────────────────────────────── */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }

    /* ─── Hero Section ─────────────────────────────────────────── */
    .hero-container {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.2) 0%, rgba(6, 182, 212, 0.2) 50%, rgba(244, 114, 182, 0.2) 100%);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        backdrop-filter: blur(12px);
        animation: fadeInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(124, 58, 237, 0.08) 0%, transparent 60%);
        animation: rotate 20s linear infinite;
    }

    .hero-container h1 {
        background: linear-gradient(135deg, #A78BFA, #06B6D4, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }

    .hero-container p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        position: relative;
        z-index: 1;
    }

    /* ─── Glass Cards ──────────────────────────────────────────── */
    .glass-card {
        background: var(--bg-glass);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-glow);
        border-color: rgba(124, 58, 237, 0.3);
    }

    .glass-card h3 {
        color: var(--text-primary) !important;
        font-size: 1.2rem !important;
        margin-bottom: 0.5rem;
    }

    .glass-card p {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* ─── Career Cards ─────────────────────────────────────────── */
    .career-card {
        background: var(--bg-glass);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 1.8rem;
        margin-bottom: 1.2rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .career-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 40px rgba(124, 58, 237, 0.2);
        border-color: var(--primary-light);
    }

    .career-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--gradient-primary);
        border-radius: 4px 0 0 4px;
    }

    .career-card .match-badge {
        display: inline-block;
        background: var(--gradient-primary);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    .career-card .career-title {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.5rem;
    }

    .career-card .career-desc {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    .career-card .skill-tag {
        display: inline-block;
        background: rgba(124, 58, 237, 0.15);
        color: var(--primary-light);
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        border: 1px solid rgba(124, 58, 237, 0.25);
    }

    .career-card .growth-badge {
        display: inline-block;
        background: rgba(6, 182, 212, 0.15);
        color: var(--secondary);
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }

    .career-card .salary-badge {
        display: inline-block;
        background: rgba(244, 114, 182, 0.15);
        color: var(--accent);
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 0.5rem;
        margin-left: 0.3rem;
    }

    /* ─── Score Section ─────────────────────────────────────────── */
    .score-container {
        text-align: center;
        padding: 2rem;
    }

    .verdict-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 30px;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-top: 1rem;
    }

    .verdict-ready { background: rgba(34, 197, 94, 0.2); color: #22C55E; border: 1px solid rgba(34, 197, 94, 0.3); }
    .verdict-almost { background: rgba(6, 182, 212, 0.2); color: #06B6D4; border: 1px solid rgba(6, 182, 212, 0.3); }
    .verdict-needs { background: rgba(245, 158, 11, 0.2); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3); }
    .verdict-starting { background: rgba(244, 114, 182, 0.2); color: #F472B6; border: 1px solid rgba(244, 114, 182, 0.3); }

    /* ─── Skill Gap Table ──────────────────────────────────────── */
    .skill-have {
        background: rgba(34, 197, 94, 0.12);
        border-left: 3px solid #22C55E;
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        color: var(--text-primary);
        font-size: 0.95rem;
    }

    .skill-need {
        background: rgba(245, 158, 11, 0.12);
        border-left: 3px solid #F59E0B;
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        color: var(--text-primary);
        font-size: 0.95rem;
    }

    .skill-level {
        float: right;
        font-size: 0.8rem;
        color: var(--text-secondary);
        font-style: italic;
    }

    .priority-high { color: #EF4444; font-weight: 600; }
    .priority-medium { color: #F59E0B; }
    .priority-low { color: #22C55E; }

    /* ─── Roadmap Timeline ─────────────────────────────────────── */
    .roadmap-task {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        position: relative;
        padding-left: 2rem;
        transition: all 0.3s ease;
    }

    .roadmap-task:hover {
        border-color: var(--primary-light);
        transform: translateX(4px);
    }

    .roadmap-task::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 4px;
        height: 100%;
        background: var(--gradient-primary);
        border-radius: 4px 0 0 4px;
    }

    .roadmap-task .task-title {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.4rem;
    }

    .roadmap-task .task-resource {
        color: var(--secondary);
        font-size: 0.85rem;
        margin-bottom: 0.3rem;
    }

    .roadmap-task .task-milestone {
        color: var(--accent);
        font-size: 0.85rem;
        font-style: italic;
    }

    /* ─── Chat Styling ─────────────────────────────────────────── */
    .chat-suggestion {
        display: inline-block;
        background: rgba(124, 58, 237, 0.12);
        border: 1px solid rgba(124, 58, 237, 0.25);
        color: var(--primary-light);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.3rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .chat-suggestion:hover {
        background: rgba(124, 58, 237, 0.25);
        transform: translateY(-2px);
    }

    /* ─── Form Styling ─────────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        border-radius: var(--radius-sm) !important;
        border-color: var(--border-subtle) !important;
        transition: border-color 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within,
    .stMultiSelect > div > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 1px var(--primary) !important;
    }

    /* ─── Button Styling ───────────────────────────────────────── */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.7rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.3px !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ─── Tabs Styling ─────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--bg-surface);
        border-radius: var(--radius-md);
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm);
        padding: 0.5rem 1.5rem;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
    }

    /* ─── Sidebar ──────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E1B4B 100%);
        border-right: 1px solid var(--border-subtle);
    }

    /* ─── Animations ───────────────────────────────────────────── */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* Stagger animation delays for cards */
    .glass-card:nth-child(1) { animation-delay: 0.1s; }
    .glass-card:nth-child(2) { animation-delay: 0.2s; }
    .glass-card:nth-child(3) { animation-delay: 0.3s; }

    /* ─── Metric Cards ─────────────────────────────────────────── */
    .metric-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        border-color: var(--primary-light);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .metric-label {
        color: var(--text-secondary);
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }

    /* ─── Section Headers ──────────────────────────────────────── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border-subtle);
    }

    .section-header h2 {
        font-size: 1.4rem !important;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ─── Hide Streamlit defaults ──────────────────────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
"""

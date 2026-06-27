# 💜 CareerHer — AI Career Counselor for Women

An AI-powered career counseling platform designed to help women restart their careers after a break. Built with **FastAPI** (backend) and **Streamlit** (frontend), powered by **Google Gemini 1.5 Flash**.

## ✨ Features

- **📝 Intake Form** — Comprehensive profile with skills, interests, and goals
- **📊 Results Dashboard** — Employability score gauge, 3 career cards, skill gap table, 30/60/90 day roadmap
- **💬 AI Career Coach** — Chat with a personalized career counselor
- **🤖 AI-Powered** — Google Gemini 1.5 Flash provides intelligent, context-aware responses
- **🎨 Premium UI** — Glassmorphism design with dark theme and smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google API Key from [Google AI Studio](https://aistudio.google.com/apikey)

### Setup

1. **Clone the repo:**
   ```bash
   git clone <your-repo-url>
   cd womens-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   pip install -r frontend/requirements.txt
   ```

3. **Set your API key:**
   ```bash
   # Edit backend/.env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

4. **Start the backend:**
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

5. **Start the frontend** (in a new terminal):
   ```bash
   cd frontend
   streamlit run 🏠_Home.py --server.port 8501
   ```

6. **Open** http://localhost:8501 in your browser

## 📁 Project Structure

```
womens ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Settings & env management
│   │   ├── api/endpoints.py     # /analyze, /score, /roadmap, /chat
│   │   ├── schemas/             # Pydantic request/response models
│   │   ├── services/            # Gemini AI service & business logic
│   │   └── prompts/templates.py # AI prompt templates
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── 🏠_Home.py               # Intake form
│   ├── pages/
│   │   ├── 1_📊_Results.py      # Results dashboard
│   │   └── 2_💬_Chat.py         # AI chat
│   ├── utils/                   # API client, styles, state management
│   └── .streamlit/config.toml   # Theme configuration
├── .gitignore
└── README.md
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/catalogs` | Skills & interests lists |
| POST | `/analyze` | Career analysis & recommendations |
| POST | `/score` | Employability scoring |
| POST | `/roadmap` | 30/60/90 day action plan |
| POST | `/chat` | AI career coaching chat |

## 🌐 Deployment

### Streamlit Cloud (Frontend)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → Deploy

### Render (Backend)
1. Go to [render.com](https://render.com)
2. New Web Service → Connect repo
3. Set build command: `pip install -r backend/requirements.txt`
4. Set start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 📄 License

MIT License — built with 💜 for women restarting their careers.

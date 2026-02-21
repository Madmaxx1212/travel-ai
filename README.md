# 🛫 AI Travel Guardian+ 

> **LLM + ML powered intelligent travel planning system**  
> MSc Big Data Analytics — Final Year Project

An end-to-end AI-powered travel planning web application that combines XGBoost flight delay prediction, VADER/DistilBERT sentiment analysis, FAISS-based RAG, and a 7-agent LangGraph system — all powered by Groq LLM.

---

## ✨ Key Features

| Feature | Technology |
|---------|-----------|
| **Flight Delay Prediction** | XGBoost + 13 engineered features |
| **Airline Sentiment Analysis** | VADER NLP on 200+ reviews |
| **Customer Convenience Score** | Weighted CCS formula with priority presets |
| **Explainable AI** | SHAP TreeExplainer for prediction transparency |
| **Risk Warnings** | Rule-based + LLM-powered flight risk alerts |
| **Hotel Recommendations** | Budget/safety/rating scoring + LLM personalization |
| **Day-wise Itinerary** | City knowledge RAG + LLM generation |
| **Dynamic Replanning** | Change dates, budget, destination mid-conversation |
| **Real-time Chat** | WebSocket streaming with 7-agent pipeline |

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│                    React Frontend                     │
│   Landing Page → Chat (WebSocket) → Trip Dashboard   │
│     Tailwind CSS · Framer Motion · Zustand · Recharts│
└───────────────────────┬──────────────────────────────┘
                        │ WebSocket / REST
┌───────────────────────┴──────────────────────────────┐
│                  FastAPI Backend                       │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │            7-Agent LangGraph Pipeline            │ │
│  │  Intent → Flight → Risk → Explain →             │ │
│  │  Hotel → Itinerary → Replan                     │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌──────────┐  ┌────────────┐  ┌─────────────────┐  │
│  │ XGBoost  │  │ VADER NLP  │  │ FAISS + sentence│  │
│  │ Delay ML │  │ Sentiment  │  │  transformers   │  │
│  └──────────┘  └────────────┘  └─────────────────┘  │
│                                                       │
│  ┌──────────┐  ┌────────────┐  ┌─────────────────┐  │
│  │ Groq LLM │  │   SQLite   │  │ SHAP Explainer  │  │
│  │  Client  │  │  Database  │  │                 │  │
│  └──────────┘  └────────────┘  └─────────────────┘  │
└──────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- [Groq API Key](https://console.groq.com/) (free tier available)

### 1. Backend Setup

```bash
# Create virtual environment
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux
# Edit .env and add your GROQ_API_KEY

# Seed database + train model (happens automatically on first run)
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 3. Open the App
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Docker (Alternative)
```bash
docker-compose up --build
```

## 📁 Project Structure

```
ai-travel/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py             # Pydantic settings
│   ├── api/                  # REST + WebSocket endpoints
│   ├── agents/               # 7 LangGraph agents + graph wiring
│   ├── ml/                   # XGBoost, VADER, CCS, SHAP
│   ├── rag/                  # FAISS embedder + retriever
│   ├── llm/                  # Groq client + prompt templates
│   ├── database/             # SQLAlchemy models + seed data
│   └── utils/                # Logging + helpers
├── frontend/
│   └── src/
│       ├── components/       # 20+ React components
│       ├── pages/            # Landing, Chat, Dashboard, Login
│       ├── store/            # Zustand global state
│       └── lib/              # API client + WebSocket wrapper
├── data/                     # City knowledge + generated CSVs
└── docker-compose.yml
```

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | **Required** — Get from [console.groq.com](https://console.groq.com/) |
| `DATABASE_URL` | SQLite path (default: `sqlite:///./travel_guardian.db`) |
| `JWT_SECRET_KEY` | JWT signing key (any random string) |

## 🧪 Tech Stack

**Backend:** FastAPI · SQLAlchemy · XGBoost · SHAP · VADER · FAISS · sentence-transformers · LangGraph · Groq API  
**Frontend:** React 18 · Vite · Tailwind CSS · Framer Motion · Zustand · Recharts · Lucide Icons  
**Infrastructure:** SQLite · Docker · WebSockets

---

*Built with ❤️ as MSc Big Data Analytics Final Year Project*

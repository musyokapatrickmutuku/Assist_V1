# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Assist AI** is a medical AI assistant platform designed to help diabetes patients communicate with healthcare providers through AI-assisted query processing. The system uses a human-in-the-loop approach where AI generates draft responses that doctors review and approve before sending to patients.

## Architecture

### Core Components

1. **Backend Service** (`backend_service/`)
   - **FastAPI application** (`main.py`) - REST API with CORS middleware
   - **LangGraph workflow** (`graph.py`) - Multi-node AI processing pipeline
   - **SQLite database** (`patient_db.py`) - Patient data and query storage
   - **Pydantic schemas** (`schemas.py`) - Data validation models

2. **Frontend Application** (`frontend/streamlit_app/`)
   - **Streamlit web app** (`main.py`) - Main entry point with role-based routing
   - **Patient portal** (`patient.py`) - Query submission interface
   - **Doctor portal** (`doctor.py`) - Query review and approval interface

### Data Flow

1. Patient submits query via Streamlit frontend
2. Backend processes query through LangGraph nodes:
   - `fetch_patient_data` - Retrieves patient medical history
   - `generate_ai_response` - Creates AI draft using DeepSeek LLM
   - `evaluate_response` - Calculates safety/confidence scores and urgency
   - `prepare_for_doctor_review` - Saves to database for doctor review
3. Doctor reviews AI draft and approves/edits response
4. Final response sent to patient

## Development Commands

### Starting the Application
```bash
# Quick setup (requires Docker)
./setup.sh

# Manual Docker setup
docker-compose up --build

# Development mode
# Backend: cd backend_service && python main.py
# Frontend: cd frontend/streamlit_app && streamlit run main.py
```

### Database Operations
```bash
# Initialize database
python backend_service/patient_db.py

# Database location: backend_service/queries.db
```

## Key Configuration

### Environment Variables (backend_service/.env)
- `DEEPSEEK_API_KEY` - Required for AI responses
- `DEEPSEEK_API_BASE` - API endpoint URL
- `DB_PATH` - Database file path (defaults to queries.db)

### Demo Accounts
**Patients:**
- P001: Sarah Johnson (Type 2 diabetes)
- P002: Michael Thompson (Type 1 diabetes)  
- P003: Carlos Rodriguez (Type 2 with complications)
- P004: Priya Patel (Pregnant with Type 2)
- P005: Eleanor Williams (Elderly with CKD)

**Doctors:**
- D001: Dr. Emily Chen
- D002: Dr. Michael Roberts

## AI Processing Pipeline

The system uses **LangGraph** for structured AI workflow:

1. **Safety Scoring** - Evaluates AI responses for medical safety (0-100)
2. **Confidence Scoring** - Measures response quality based on patient context (0-100)  
3. **Urgency Classification** - Categorizes queries as high/medium/low priority
4. **Pre-crafted Responses** - Uses template responses for common diabetes scenarios

## Database Schema

```sql
-- Queries table
CREATE TABLE queries (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    original_query TEXT NOT NULL,
    ai_response TEXT,
    doctor_final_response TEXT,
    status TEXT NOT NULL,
    urgency_level TEXT DEFAULT 'low',
    safety_score INTEGER,
    confidence_score INTEGER
);
```

## Important Implementation Notes

- **Patient data is hardcoded** in `patient_db.py` for demo purposes
- **LLM integration** uses OpenAI-compatible wrapper for DeepSeek API
- **Safety-first design** - No AI response reaches patients without doctor approval
- **Docker deployment** uses separate containers for frontend/backend
- **CORS enabled** for development (all origins allowed)

## File Structure Reference

```
├── backend_service/          # FastAPI backend
│   ├── main.py              # API endpoints
│   ├── graph.py             # LangGraph workflow
│   ├── patient_db.py        # Data management
│   ├── schemas.py           # Pydantic models
│   └── requirements.txt     # Python dependencies
├── frontend/streamlit_app/   # Streamlit frontend  
│   ├── main.py              # Main app with auth
│   ├── patient.py           # Patient interface
│   ├── doctor.py            # Doctor interface
│   └── requirements.txt     # Python dependencies
├── docker-compose.yml       # Container orchestration
└── setup.sh                # Quick start script
```
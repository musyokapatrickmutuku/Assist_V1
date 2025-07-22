# 🏥 Assist AI - Bridging the Care Gap in Chronic Disease Management

## 🎯 Problem We Solve

**422 million people** worldwide live with diabetes. Each faces:
- 📅 **3-week average wait** for non-emergency consultations
- 😰 **78% experience anxiety** about unaddressed symptoms
- 📞 **Doctors receive 50+ routine calls daily**

**Assist AI** is a human-in-the-loop platform that enables doctors to provide timely, verified responses to patient queries through AI-assisted drafts.

## 🚀 Quick Demo

```bash
# Clone the repository
git clone https://github.com/musyokapatrickmutuku/Assist_V1.git
cd Assist_V1

# Quick setup (recommended)
./setup.sh

# Or manual setup:
# Copy environment template
cp .env.example backend_service/.env
# Edit .env and add your DeepSeek API key

# Run with Docker
docker-compose up

# Access the app
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
```

## 🌟 Key Features

### For Patients
- 📝 **Submit queries** with medical context
- 📎 **Upload documents** (lab results, glucose logs)
- ⏱️ **Get responses in hours**, not weeks
- 📊 **Track query history** and health metrics

### For Doctors
- 🤖 **AI-generated draft responses** based on patient history
- 🔍 **Full patient context** at a glance
- 🚨 **Urgency indicators** (High/Medium/Low)
- ✅ **Complete control** - edit, approve, or rewrite

### Safety First
- 💯 **100% doctor verification** - No AI response reaches patients without approval
- 🛡️ **Safety scoring** - AI responses evaluated for medical safety
- 📋 **Audit trail** - Complete history of all interactions
- 🔒 **HIPAA-ready architecture** (for production)

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Patient Portal │────▶│   Backend API   │────▶│  Doctor Portal  │
│   (Streamlit)   │     │  (FastAPI +     │     │   (Streamlit)   │
│                 │     │   LangGraph)    │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                        │                        │
         │                        │                        │
         └────────────────────────▼────────────────────────┘
                          ┌─────────────────┐
                          │                 │
                          │ SQLite Database │
                          │   + Patient DB  │
                          │                 │
                          └─────────────────┘
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: FastAPI + LangGraph (AI workflow orchestration)
- **AI**: DeepSeek LLM via OpenAI-compatible API
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Deployment**: Docker + Docker Compose

## 📋 Demo Accounts

### Patients
- **P001**: Sarah Johnson (Type 2, well-controlled)
- **P002**: Michael Thompson (Type 1, college student)
- **P003**: Carlos Rodriguez (Type 2 with complications)
- **P004**: Priya Patel (Pregnant with Type 2)
- **P005**: Eleanor Williams (Elderly with CKD)

### Doctors
- **D001**: Dr. Emily Chen
- **D002**: Dr. Michael Roberts
- **Password**: `demo123` (for all accounts)

## 🔧 Development

### Prerequisites
- Docker & Docker Compose
- Python 3.9+ (for local development)
- DeepSeek API key

### Local Development
```bash
# Backend development
cd backend_service
pip install -r requirements.txt
python main.py

# Frontend development  
cd frontend/streamlit_app
pip install -r requirements.txt
streamlit run main.py
```

### Environment Variables
```bash
# Required in backend_service/.env
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_BASE=https://api.novita.ai/v3/openai
DB_PATH=queries.db
```

## 🚀 Deployment

### Docker (Recommended)
```bash
docker-compose up --build
```

### Production Considerations
- Use PostgreSQL instead of SQLite
- Configure HTTPS with proper certificates
- Set up proper authentication and session management
- Implement HIPAA compliance measures
- Add monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for improving healthcare accessibility
- AI-powered but human-verified approach
- Designed with patient safety as the top priority

---

**⚠️ Disclaimer**: This is a demonstration platform. For production medical use, additional safety measures, certifications, and regulatory compliance are required.
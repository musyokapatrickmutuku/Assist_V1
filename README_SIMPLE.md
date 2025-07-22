# Assist AI - Simplified MVP Demo

A simplified version of the medical AI assistant platform focusing on core functionality without complex AI processing.

## What This Demo Does

### For Patients:
- Submit medical questions easily
- See immediate confirmation when questions are sent
- Track question status (pending/answered)
- View doctor responses

### For Doctors:
- See all pending patient questions
- Prioritize by urgency (high/medium/low)
- Send responses with quick templates
- Simple, clean interface

## Key Simplifications

1. **No LangGraph**: Removed complex AI workflow processing
2. **Simple Database**: Direct SQLite operations instead of complex schemas
3. **Direct Communication**: No intermediate AI analysis
4. **Focused UI**: Clean, minimal interface for core tasks
5. **Fast Setup**: No external dependencies or API keys needed

## Quick Start

### Method 1: Batch Files (Recommended)
1. Double-click `run_simple_backend.bat` (starts on port 8001)
2. Double-click `run_simple_frontend.bat` (opens browser on port 8502)

### Method 2: Manual
1. **Start Backend:**
   ```bash
   cd backend_service
   python main_simple.py
   ```

2. **Start Frontend:**
   ```bash
   cd frontend/streamlit_app
   set BACKEND_URL=http://localhost:8001
   streamlit run app_simple.py --server.port 8502
   ```

## Demo Flow

1. **Login as Patient:**
   - Select "Sarah Johnson" or any demo patient
   - Click "Login"

2. **Submit Question:**
   - Type a medical question
   - Select urgency level
   - Click "Send to Doctor"
   - See confirmation message and balloons!

3. **Login as Doctor:**
   - Logout and select "Doctor"
   - Click "Login"

4. **Review Questions:**
   - See pending questions with urgency indicators
   - Use quick response templates
   - Send response to patient

5. **Verify Patient Received Response:**
   - Login back as patient
   - Check "My Questions" to see doctor's response

## Features Working

✅ Patient question submission  
✅ Question confirmation messages  
✅ Doctor review interface  
✅ Response sending  
✅ Question status tracking  
✅ Urgency prioritization  
✅ Real-time updates  

## Database

The app creates `simple_queries.db` automatically with this schema:

```sql
CREATE TABLE simple_queries (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    patient_name TEXT,
    question TEXT NOT NULL,
    doctor_response TEXT,
    status TEXT DEFAULT 'pending',
    urgency TEXT DEFAULT 'low',
    date TEXT NOT NULL
);
```

## Next Steps for Full Version

Once this simplified version works perfectly:

1. Add AI response generation (OpenAI/DeepSeek)
2. Implement safety scoring
3. Add patient medical history context
4. Implement LangGraph workflow
5. Add file upload capability
6. Add appointment scheduling
7. Add analytics dashboard

## Files Structure

```
Assist_V1/
├── backend_service/
│   └── main_simple.py          # Simplified backend
├── frontend/streamlit_app/
│   ├── app_simple.py           # Simplified main app
│   ├── patient_simple.py       # Simplified patient portal
│   └── doctor_simple.py        # Simplified doctor portal
├── run_simple_backend.bat      # Backend startup script
├── run_simple_frontend.bat     # Frontend startup script
└── README_SIMPLE.md            # This file
```

## Troubleshooting

- **Backend not starting**: Check if port 8001 is free
- **Frontend not connecting**: Ensure backend is running first
- **Database errors**: Delete `simple_queries.db` to reset
- **Import errors**: Make sure you're in the correct directory

This simplified version removes all complexity and focuses on the core user experience of patients asking questions and doctors responding - exactly what you need for a working MVP demo!

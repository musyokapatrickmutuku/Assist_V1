@echo off
echo Starting Assist AI Simple Frontend...
echo Make sure backend is running first on http://localhost:8002
echo Frontend will open at http://localhost:8506
echo Press Ctrl+C to stop the frontend
echo.
cd frontend\streamlit_app
set BACKEND_URL=http://localhost:8002
streamlit run app_simple.py --server.port 8506
pause